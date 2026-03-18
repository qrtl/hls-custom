import collections
import datetime as dt
import json
import logging

from odoo import SUPERUSER_ID, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


_logger = logging.getLogger(__name__)


BAD_QTY_SQL = """
    SELECT DISTINCT company_id, product_id
    FROM stock_valuation_layer
    WHERE
        (COALESCE(quantity, 0) = 0 AND COALESCE(remaining_qty, 0) <> 0)
        OR (ABS(COALESCE(remaining_qty, 0)) - ABS(COALESCE(quantity, 0)) > 1e-9)
"""

QTY_GAP_SQL = """
    WITH svl AS (
        SELECT
            company_id,
            product_id,
            COALESCE(SUM(remaining_qty), 0) AS rem_qty_sum
        FROM stock_valuation_layer
        GROUP BY company_id, product_id
    ),
    quant AS (
        SELECT
            sq.company_id,
            sq.product_id,
            COALESCE(SUM(sq.quantity), 0) AS quant_qty
        FROM stock_quant sq
        JOIN stock_location sl ON sl.id = sq.location_id
        WHERE
            sl.usage = 'internal'
            OR (sl.usage = 'transit' AND sl.company_id IS NOT NULL)
        GROUP BY sq.company_id, sq.product_id
    )
    SELECT svl.company_id, svl.product_id
    FROM svl
    LEFT JOIN quant
        ON quant.company_id = svl.company_id
       AND quant.product_id = svl.product_id
    WHERE ABS(COALESCE(quant.quant_qty, 0) - svl.rem_qty_sum) > 1e-9
"""


class StockSvlRemainingRepairService(models.AbstractModel):
    _name = "stock.svl.remaining.repair.service"
    _description = "Stock SVL Remaining Repair Service"

    _DONE_PARAM = "stock_svl_remaining_repair.done_at"
    _SUMMARY_PARAM = "stock_svl_remaining_repair.summary"
    _DEFAULT_REASON = "SVL remaining repair"
    _DEFAULT_ADJUSTMENT_ACCOUNT_ID = 83
    _EXCLUDED_DEFAULT_CODES = {"9999", "9901"}
    _KNOWN_QUANTITY_FIXES = (
        {
            "default_code": "86406",
            "description": "INV:2022年6月末棚卸_ヒューテック臨海第2",
            "return_description": "INV:2022年6月末棚卸_ヒューテック臨海第2_戻し",
            "note": "Fix broken inventory-adjustment SVL quantity before remaining repair.",
        },
    )

    def run_post_init_repair(self):
        params = self.env["ir.config_parameter"].sudo()
        if params.get_param(self._DONE_PARAM):
            return {
                "skipped": True,
                "reason": "already_done",
                "done_at": params.get_param(self._DONE_PARAM),
            }

        report = self.run_repair(
            adjustment_account_id=self._DEFAULT_ADJUSTMENT_ACCOUNT_ID,
            reason=self._DEFAULT_REASON,
            excluded_default_codes=self._EXCLUDED_DEFAULT_CODES,
        )
        summary = self._compact_summary(report)
        params.set_param(self._DONE_PARAM, fields.Datetime.now())
        params.set_param(self._SUMMARY_PARAM, json.dumps(summary, ensure_ascii=False, default=str))
        return summary

    def run_repair(self, adjustment_account_id, reason, excluded_default_codes=None):
        excluded_default_codes = set(excluded_default_codes or [])
        stamp = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        quantity_fix_info, forced_keys = self._apply_known_quantity_fixes(stamp)

        keys = set(self._fetch_target_keys())
        keys.update(forced_keys)
        keys = self._filter_keys(keys, excluded_default_codes=excluded_default_codes)

        plans, svl_updates, adjustments, price_updates, unsupported = self._build_plan(sorted(keys), reason=reason)
        if unsupported:
            raise UserError(
                "Unsupported products found during stock_svl_remaining_repair:\n%s"
                % json.dumps(unsupported, ensure_ascii=False, indent=2)
            )

        self._validate_apply_requirements(
            adjustments,
            adjustment_account_id=adjustment_account_id,
        )
        backup_tables = self._create_backup_tables(stamp, svl_updates, price_updates)
        if quantity_fix_info["backup_table"]:
            backup_tables["quantity_fix_backup_table"] = quantity_fix_info["backup_table"]

        self._apply_svl_updates(svl_updates)
        created_adjustments = self._apply_adjustments(
            adjustments,
            adjustment_account_id=adjustment_account_id,
            move_date=fields.Date.today(),
        )
        self._log_created_adjustments(backup_tables["adjustment_log_table"], created_adjustments)
        self._apply_price_updates(price_updates)

        report = self._build_report(
            keys=sorted(keys),
            plans=plans,
            svl_updates=svl_updates,
            adjustments=adjustments,
            price_updates=price_updates,
            apply=True,
            backup_tables=backup_tables,
            created_adjustments=created_adjustments,
        )
        report["known_quantity_fixes"] = quantity_fix_info["rows"]
        return report

    def _compact_summary(self, report):
        return {
            "db": self.env.cr.dbname,
            "target_count": report["target_count"],
            "svl_update_count": report["svl_update_count"],
            "adjustment_count": report["adjustment_count"],
            "price_update_count": report["price_update_count"],
            "backup_tables": report["backup_tables"],
            "known_quantity_fixes": report.get("known_quantity_fixes", []),
            "adjustments": [
                {
                    "product_id": row["product_id"],
                    "created_svl_id": row["created_svl_id"],
                    "created_account_move_id": row["created_account_move_id"],
                }
                for row in report.get("created_adjustments", [])
            ],
        }

    def _normalize_qty(self, product, qty):
        rounding = product.uom_id.rounding or 0.0001
        if float_is_zero(qty, precision_rounding=rounding):
            return 0.0
        return qty

    def _normalize_value(self, company, value):
        rounding = company.currency_id.rounding or 0.01
        value = company.currency_id.round(value)
        if float_is_zero(value, precision_rounding=rounding):
            return 0.0
        return value

    def _qty_row_is_bad(self, product, quantity, remaining_qty):
        rounding = product.uom_id.rounding or 0.0001
        if float_is_zero(quantity, precision_rounding=rounding):
            return not float_is_zero(remaining_qty, precision_rounding=rounding)
        return float_compare(abs(remaining_qty), abs(quantity), precision_rounding=rounding) > 0

    def _get_product_metadata(self, company_id, product_id):
        product = self.env["product.product"].browse(product_id).with_company(company_id)
        company = self.env["res.company"].browse(company_id)
        return product, company

    def _fetch_sql_keys(self, sql, product_ids=None):
        query = "SELECT company_id, product_id FROM (%s) AS target_keys" % sql
        params = []
        if product_ids:
            query += " WHERE product_id = ANY(%s)"
            params.append(product_ids)
        query += " ORDER BY company_id, product_id"
        self.env.cr.execute(query, tuple(params))
        return [(company_id, product_id) for company_id, product_id in self.env.cr.fetchall()]

    def _fetch_target_keys(self, product_ids=None):
        if product_ids:
            self.env.cr.execute(
                """
                SELECT DISTINCT company_id, product_id
                FROM stock_valuation_layer
                WHERE product_id = ANY(%s)
                ORDER BY company_id, product_id
                """,
                (product_ids,),
            )
            return [(company_id, product_id) for company_id, product_id in self.env.cr.fetchall()]
        keys = set(self._fetch_sql_keys(BAD_QTY_SQL, product_ids=product_ids))
        for company_id, product_id in self._fetch_sql_keys(QTY_GAP_SQL, product_ids=product_ids):
            product, _company = self._get_product_metadata(company_id, product_id)
            if product.cost_method == "fifo":
                keys.add((company_id, product_id))
        return sorted(keys)

    def _filter_keys(self, keys, excluded_default_codes=None):
        excluded_default_codes = set(excluded_default_codes or [])
        filtered = []
        for company_id, product_id in keys:
            product, _company = self._get_product_metadata(company_id, product_id)
            if product.default_code in excluded_default_codes:
                continue
            filtered.append((company_id, product_id))
        return filtered

    def _fetch_quant_qty_map(self, keys):
        if not keys:
            return {}
        product_ids = sorted({product_id for _, product_id in keys})
        company_ids = sorted({company_id for company_id, _ in keys})
        self.env.cr.execute(
            """
            SELECT
                sq.company_id,
                sq.product_id,
                COALESCE(SUM(sq.quantity), 0)
            FROM stock_quant sq
            JOIN stock_location sl ON sl.id = sq.location_id
            WHERE sq.product_id = ANY(%s)
              AND sq.company_id = ANY(%s)
              AND (
                  sl.usage = 'internal'
                  OR (sl.usage = 'transit' AND sl.company_id IS NOT NULL)
              )
            GROUP BY sq.company_id, sq.product_id
            """,
            (product_ids, company_ids),
        )
        return {
            (company_id, product_id): qty
            for company_id, product_id, qty in self.env.cr.fetchall()
        }

    def _fetch_svl_rows(self, company_id, product_id):
        self.env.cr.execute(
            """
            SELECT
                id,
                quantity,
                value,
                COALESCE(remaining_qty, 0),
                COALESCE(remaining_value, 0),
                create_date,
                description
            FROM stock_valuation_layer
            WHERE company_id = %s
              AND product_id = %s
            ORDER BY create_date, id
            """,
            (company_id, product_id),
        )
        rows = []
        for svl_id, quantity, value, remaining_qty, remaining_value, create_date, description in self.env.cr.fetchall():
            rows.append(
                {
                    "id": svl_id,
                    "quantity": quantity or 0.0,
                    "value": value or 0.0,
                    "remaining_qty": remaining_qty or 0.0,
                    "remaining_value": remaining_value or 0.0,
                    "create_date": create_date,
                    "description": description or "",
                }
            )
        return rows

    def _summarize_key(self, company_id, product_id, quant_qty=None):
        product, company = self._get_product_metadata(company_id, product_id)
        rows = self._fetch_svl_rows(company_id, product_id)
        qty_sum = 0.0
        value_sum = 0.0
        rem_qty_sum = 0.0
        rem_value_sum = 0.0
        bad_qty_rows = 0
        nonzero_remaining_rows = 0
        for row in rows:
            qty_sum += row["quantity"]
            value_sum += row["value"]
            rem_qty_sum += row["remaining_qty"]
            rem_value_sum += row["remaining_value"]
            if self._qty_row_is_bad(product, row["quantity"], row["remaining_qty"]):
                bad_qty_rows += 1
            if (
                not float_is_zero(row["remaining_qty"], precision_rounding=product.uom_id.rounding)
                or not float_is_zero(row["remaining_value"], precision_rounding=company.currency_id.rounding)
            ):
                nonzero_remaining_rows += 1
        if quant_qty is None:
            quant_qty = self._fetch_quant_qty_map([(company_id, product_id)]).get((company_id, product_id), 0.0)
        return {
            "company_id": company_id,
            "product_id": product_id,
            "default_code": product.default_code,
            "name": product.display_name,
            "is_storable": bool(product.is_storable),
            "cost_method": product.cost_method,
            "valuation": product.valuation,
            "quant_qty": quant_qty,
            "quantity_sum": self._normalize_qty(product, qty_sum),
            "value_sum": self._normalize_value(company, value_sum),
            "remaining_qty_sum": self._normalize_qty(product, rem_qty_sum),
            "remaining_value_sum": self._normalize_value(company, rem_value_sum),
            "qty_gap": self._normalize_qty(product, quant_qty - rem_qty_sum),
            "bad_qty_rows": bad_qty_rows,
            "nonzero_remaining_rows": nonzero_remaining_rows,
            "standard_price": product.standard_price,
        }

    def _check_supported(self, company_id, product_id, before):
        product, company = self._get_product_metadata(company_id, product_id)
        svl_model = self.env["stock.valuation.layer"]
        has_landed_cost = "stock_landed_cost_id" in svl_model._fields

        if product.cost_method == "fifo":
            if product.lot_valuated:
                return "lot_valuated product is not supported"
            if float_compare(before["quantity_sum"], before["quant_qty"], precision_rounding=product.uom_id.rounding) != 0:
                return "sum(quantity) and quant qty differ"
            domains = [
                [
                    ("company_id", "=", company_id),
                    ("product_id", "=", product_id),
                    ("stock_valuation_layer_id", "!=", False),
                ],
                [
                    ("company_id", "=", company_id),
                    ("product_id", "=", product_id),
                    ("quantity", "=", 0),
                    ("description", "like", "Manual Stock Valuation:%"),
                ],
                [
                    ("company_id", "=", company_id),
                    ("product_id", "=", product_id),
                    ("remaining_qty", "<", 0),
                ],
            ]
            if has_landed_cost:
                domains.append(
                    [
                        ("company_id", "=", company_id),
                        ("product_id", "=", product_id),
                        ("stock_landed_cost_id", "!=", False),
                    ]
                )
            if any(svl_model.sudo().search_count(domain) for domain in domains):
                return "linked adjustments, landed costs, or open negative stock detected"
            return None

        rows = self._fetch_svl_rows(company_id, product_id)
        if not float_is_zero(before["quant_qty"], precision_rounding=product.uom_id.rounding):
            return "non-fifo residual cleanup requires zero quant quantity"
        if any(not float_is_zero(row["value"], precision_rounding=company.currency_id.rounding) for row in rows):
            return "non-fifo residual cleanup requires all SVL values to be zero"
        return None

    def _plan_fifo_product(self, company_id, product_id, value_sum_target=None):
        product, company = self._get_product_metadata(company_id, product_id)
        rows = self._fetch_svl_rows(company_id, product_id)
        queue = collections.deque()
        states = {}

        for row in rows:
            quantity = row["quantity"]
            if float_compare(quantity, 0.0, precision_rounding=product.uom_id.rounding) > 0:
                state = {
                    "remaining_qty": self._normalize_qty(product, quantity),
                    "remaining_value": self._normalize_value(company, row["value"]),
                }
                states[row["id"]] = state
                queue.append(state)
                continue

            if float_compare(quantity, 0.0, precision_rounding=product.uom_id.rounding) < 0:
                qty_to_take = self._normalize_qty(product, abs(quantity))
                while qty_to_take and queue:
                    candidate = queue[0]
                    take = min(candidate["remaining_qty"], qty_to_take)
                    candidate_unit_cost = (
                        candidate["remaining_value"] / candidate["remaining_qty"] if candidate["remaining_qty"] else 0.0
                    )
                    taken_value = company.currency_id.round(take * candidate_unit_cost)
                    candidate["remaining_qty"] = self._normalize_qty(product, candidate["remaining_qty"] - take)
                    candidate["remaining_value"] = self._normalize_value(company, candidate["remaining_value"] - taken_value)
                    qty_to_take = self._normalize_qty(product, qty_to_take - take)
                    if float_is_zero(candidate["remaining_qty"], precision_rounding=product.uom_id.rounding):
                        queue.popleft()
                if qty_to_take:
                    raise ValueError(
                        "open negative stock is not supported for %s (svl %s, qty %s)"
                        % (product.default_code, row["id"], qty_to_take)
                    )

        rem_qty_after = 0.0
        rem_value_after = 0.0
        for row in rows:
            if float_compare(row["quantity"], 0.0, precision_rounding=product.uom_id.rounding) > 0:
                rem_qty_after += states[row["id"]]["remaining_qty"]
                rem_value_after += states[row["id"]]["remaining_value"]

        rem_qty_after = self._normalize_qty(product, rem_qty_after)
        rem_value_after = self._normalize_value(company, rem_value_after)
        if value_sum_target is not None and float_compare(rem_qty_after, 0.0, precision_rounding=product.uom_id.rounding) > 0:
            absorption = self._normalize_value(company, value_sum_target - rem_value_after)
            if not float_is_zero(absorption, precision_rounding=company.currency_id.rounding):
                for row in rows:
                    if float_compare(row["quantity"], 0.0, precision_rounding=product.uom_id.rounding) <= 0:
                        continue
                    target_qty = states[row["id"]]["remaining_qty"]
                    if float_is_zero(target_qty, precision_rounding=product.uom_id.rounding):
                        continue
                    states[row["id"]]["remaining_value"] = self._normalize_value(
                        company,
                        states[row["id"]]["remaining_value"] + absorption,
                    )
                    rem_value_after = self._normalize_value(company, rem_value_after + absorption)
                    break

        updates = []
        for row in rows:
            current_qty = row["remaining_qty"]
            current_value = row["remaining_value"]
            if float_compare(row["quantity"], 0.0, precision_rounding=product.uom_id.rounding) > 0:
                target_qty = states[row["id"]]["remaining_qty"]
                target_value = states[row["id"]]["remaining_value"]
            else:
                target_qty = 0.0
                target_value = 0.0

            qty_changed = not float_is_zero(current_qty - target_qty, precision_rounding=product.uom_id.rounding)
            value_changed = abs(current_value - target_value) > 1e-9
            if qty_changed or value_changed:
                updates.append(
                    {
                        "svl_id": row["id"],
                        "old_remaining_qty": current_qty,
                        "old_remaining_value": current_value,
                        "new_remaining_qty": target_qty,
                        "new_remaining_value": target_value,
                    }
                )

        new_standard_price = None
        if float_compare(rem_qty_after, 0.0, precision_rounding=product.uom_id.rounding) > 0:
            new_standard_price = rem_value_after / rem_qty_after

        return updates, rem_qty_after, rem_value_after, new_standard_price

    def _plan_zero_residual_product(self, company_id, product_id):
        product, company = self._get_product_metadata(company_id, product_id)
        rows = self._fetch_svl_rows(company_id, product_id)
        updates = []
        for row in rows:
            qty_changed = not float_is_zero(row["remaining_qty"], precision_rounding=product.uom_id.rounding)
            value_changed = abs(row["remaining_value"]) > 1e-9
            if qty_changed or value_changed:
                updates.append(
                    {
                        "svl_id": row["id"],
                        "old_remaining_qty": row["remaining_qty"],
                        "old_remaining_value": row["remaining_value"],
                        "new_remaining_qty": 0.0,
                        "new_remaining_value": 0.0,
                    }
                )
        return updates, 0.0, 0.0, None

    def _build_plan(self, keys, reason):
        quant_qty_map = self._fetch_quant_qty_map(keys)
        plans = []
        svl_updates = []
        adjustments = []
        price_updates = []
        unsupported = []

        for company_id, product_id in keys:
            before = self._summarize_key(company_id, product_id, quant_qty=quant_qty_map.get((company_id, product_id), 0.0))
            product, company = self._get_product_metadata(company_id, product_id)
            reason_unsupported = self._check_supported(company_id, product_id, before)
            if reason_unsupported:
                unsupported.append(
                    {
                        "company_id": company_id,
                        "product_id": product_id,
                        "default_code": before["default_code"],
                        "reason": reason_unsupported,
                    }
                )
                continue

            needs_value_alignment_adjustment = product.cost_method == "fifo" and not float_is_zero(
                before["qty_gap"],
                precision_rounding=product.uom_id.rounding,
            )

            try:
                if product.cost_method == "fifo":
                    value_sum_target = before["value_sum"] if not needs_value_alignment_adjustment else None
                    updates, rem_qty_after, rem_value_after, new_standard_price = self._plan_fifo_product(
                        company_id,
                        product_id,
                        value_sum_target=value_sum_target,
                    )
                else:
                    updates, rem_qty_after, rem_value_after, new_standard_price = self._plan_zero_residual_product(
                        company_id, product_id
                    )
            except ValueError as exc:
                unsupported.append(
                    {
                        "company_id": company_id,
                        "product_id": product_id,
                        "default_code": before["default_code"],
                        "reason": str(exc),
                    }
                )
                continue

            adjustment = None
            if needs_value_alignment_adjustment:
                value_delta = self._normalize_value(company, rem_value_after - before["value_sum"])
                if not float_is_zero(value_delta, precision_rounding=company.currency_id.rounding):
                    adjustment = {
                        "company_id": company_id,
                        "product_id": product_id,
                        "default_code": before["default_code"],
                        "name": before["name"],
                        "value_delta": value_delta,
                        "description": "Manual Stock Valuation: %s (%s)." % (reason, before["default_code"] or before["name"]),
                        "needs_account_move": before["valuation"] == "real_time",
                    }
                    adjustments.append(adjustment)

            price_update = None
            if new_standard_price is not None:
                old_standard_price = product.standard_price
                if not float_is_zero(old_standard_price - new_standard_price, precision_rounding=company.currency_id.rounding):
                    price_update = {
                        "company_id": company_id,
                        "product_id": product_id,
                        "old_standard_price": old_standard_price,
                        "new_standard_price": new_standard_price,
                    }
                    price_updates.append(price_update)

            after_value_sum = self._normalize_value(company, before["value_sum"] + (adjustment["value_delta"] if adjustment else 0.0))
            plans.append(
                {
                    "company_id": company_id,
                    "product_id": product_id,
                    "default_code": before["default_code"],
                    "name": before["name"],
                    "before": before,
                    "after": {
                        "remaining_qty_sum": rem_qty_after,
                        "remaining_value_sum": rem_value_after,
                        "qty_gap": self._normalize_qty(product, before["quant_qty"] - rem_qty_after),
                        "value_sum": after_value_sum,
                        "value_gap": self._normalize_value(company, rem_value_after - after_value_sum),
                        "bad_qty_rows": 0,
                        "standard_price": new_standard_price if new_standard_price is not None else before["standard_price"],
                    },
                    "update_count": len(updates),
                    "adjustment": adjustment,
                    "price_update": price_update,
                }
            )
            svl_updates.extend(updates)

        return plans, svl_updates, adjustments, price_updates, unsupported

    def _validate_apply_requirements(self, adjustments, adjustment_account_id=None):
        needs_moves = [row for row in adjustments if row["needs_account_move"]]
        if needs_moves and not adjustment_account_id:
            raise UserError("adjustment account is required to apply real_time valuation adjustments")

        adjustment_account = None
        if adjustment_account_id:
            adjustment_account = self.env["account.account"].browse(adjustment_account_id)
            if not adjustment_account.exists():
                raise UserError("adjustment account %s not found" % adjustment_account_id)

        for row in needs_moves:
            product, company = self._get_product_metadata(row["company_id"], row["product_id"])
            accounts = product.product_tmpl_id.get_product_accounts()
            if not accounts.get("stock_valuation"):
                raise UserError("stock valuation account is missing for %s" % (row["default_code"] or row["product_id"]))
            journal = accounts.get("stock_journal")
            if not journal:
                raise UserError("stock journal is missing for %s" % (row["default_code"] or row["product_id"]))
            if journal.company_id and journal.company_id != company:
                raise UserError("stock journal %s does not belong to company %s" % (journal.display_name, company.display_name))
            if adjustment_account:
                if "company_id" in adjustment_account._fields:
                    account_company_ok = not adjustment_account.company_id or adjustment_account.company_id == company
                else:
                    account_company_ok = not adjustment_account.company_ids or company in adjustment_account.company_ids
                if not account_company_ok:
                    raise UserError(
                        "adjustment account %s does not belong to company %s"
                        % (adjustment_account.display_name, company.display_name)
                    )

    def _create_backup_tables(self, stamp, svl_updates, price_updates):
        tables = {}

        if svl_updates:
            svl_table = "x_svl_remaining_fix_%s" % stamp
            self.env.cr.execute(
                """
                CREATE TABLE %s (
                    svl_id integer PRIMARY KEY,
                    old_remaining_qty numeric,
                    old_remaining_value numeric,
                    new_remaining_qty numeric,
                    new_remaining_value numeric,
                    backup_at timestamp without time zone
                )
                """
                % svl_table
            )
            self.env.cr.executemany(
                f"""
                INSERT INTO {svl_table} (
                    svl_id,
                    old_remaining_qty,
                    old_remaining_value,
                    new_remaining_qty,
                    new_remaining_value,
                    backup_at
                ) VALUES (%s, %s, %s, %s, %s, now())
                """,
                [
                    (
                        row["svl_id"],
                        row["old_remaining_qty"],
                        row["old_remaining_value"],
                        row["new_remaining_qty"],
                        row["new_remaining_value"],
                    )
                    for row in svl_updates
                ],
            )
            tables["svl_backup_table"] = svl_table

        adjustment_table = "x_svl_value_alignment_%s" % stamp
        self.env.cr.execute(
            """
            CREATE TABLE %s (
                company_id integer,
                product_id integer,
                value_delta numeric,
                description text,
                created_svl_id integer,
                created_account_move_id integer,
                backup_at timestamp without time zone
            )
            """
            % adjustment_table
        )
        tables["adjustment_log_table"] = adjustment_table

        if price_updates:
            price_table = "x_svl_price_fix_%s" % stamp
            self.env.cr.execute(
                """
                CREATE TABLE %s (
                    company_id integer,
                    product_id integer,
                    old_standard_price numeric,
                    new_standard_price numeric,
                    backup_at timestamp without time zone
                )
                """
                % price_table
            )
            self.env.cr.executemany(
                f"""
                INSERT INTO {price_table} (
                    company_id,
                    product_id,
                    old_standard_price,
                    new_standard_price,
                    backup_at
                ) VALUES (%s, %s, %s, %s, now())
                """,
                [
                    (
                        row["company_id"],
                        row["product_id"],
                        row["old_standard_price"],
                        row["new_standard_price"],
                    )
                    for row in price_updates
                ],
            )
            tables["price_backup_table"] = price_table

        return tables

    def _apply_svl_updates(self, svl_updates):
        if not svl_updates:
            return
        self.env.cr.executemany(
            """
            UPDATE stock_valuation_layer
            SET remaining_qty = %s,
                remaining_value = %s,
                write_date = now(),
                write_uid = %s
            WHERE id = %s
            """,
            [
                (
                    row["new_remaining_qty"],
                    row["new_remaining_value"],
                    SUPERUSER_ID,
                    row["svl_id"],
                )
                for row in svl_updates
            ],
        )

    def _create_adjustment_move(self, svl, value_delta, adjustment_account_id, move_date):
        product = svl.product_id.with_company(svl.company_id)
        accounts = product.product_tmpl_id.get_product_accounts()
        stock_valuation_account = accounts.get("stock_valuation")
        if not stock_valuation_account:
            raise UserError("stock valuation account is missing for %s" % (product.default_code or product.display_name))

        journal = accounts.get("stock_journal")
        if not journal:
            raise UserError("stock journal is missing for %s" % (product.default_code or product.display_name))

        counterpart_account = self.env["account.account"].browse(adjustment_account_id)
        amount = abs(value_delta)
        if value_delta < 0:
            debit_account = counterpart_account
            credit_account = stock_valuation_account
        else:
            debit_account = stock_valuation_account
            credit_account = counterpart_account

        line_name = "%s\nSVL remaining repair alignment" % svl.description
        move = self.env["account.move"].create(
            {
                "journal_id": journal.id,
                "company_id": svl.company_id.id,
                "ref": "SVL remaining repair %s" % (product.default_code or product.display_name),
                "stock_valuation_layer_ids": [(6, None, [svl.id])],
                "date": move_date,
                "move_type": "entry",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": line_name,
                            "account_id": debit_account.id,
                            "debit": amount,
                            "credit": 0,
                            "product_id": product.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": line_name,
                            "account_id": credit_account.id,
                            "debit": 0,
                            "credit": amount,
                            "product_id": product.id,
                        },
                    ),
                ],
            }
        )
        move._post()
        return move

    def _apply_adjustments(self, adjustments, adjustment_account_id, move_date):
        created_rows = []
        for row in adjustments:
            svl = self.env["stock.valuation.layer"].create(
                {
                    "company_id": row["company_id"],
                    "product_id": row["product_id"],
                    "description": row["description"],
                    "value": row["value_delta"],
                    "unit_cost": 0.0,
                    "quantity": 0.0,
                    "remaining_qty": 0.0,
                    "remaining_value": 0.0,
                }
            )
            account_move = None
            if row["needs_account_move"]:
                account_move = self._create_adjustment_move(
                    svl,
                    row["value_delta"],
                    adjustment_account_id=adjustment_account_id,
                    move_date=move_date,
                )
            created_rows.append(
                {
                    "company_id": row["company_id"],
                    "product_id": row["product_id"],
                    "value_delta": row["value_delta"],
                    "description": row["description"],
                    "created_svl_id": svl.id,
                    "created_account_move_id": account_move.id if account_move else None,
                }
            )
        return created_rows

    def _log_created_adjustments(self, table_name, created_rows):
        if not created_rows:
            return
        self.env.cr.executemany(
            f"""
            INSERT INTO {table_name} (
                company_id,
                product_id,
                value_delta,
                description,
                created_svl_id,
                created_account_move_id,
                backup_at
            ) VALUES (%s, %s, %s, %s, %s, %s, now())
            """,
            [
                (
                    row["company_id"],
                    row["product_id"],
                    row["value_delta"],
                    row["description"],
                    row["created_svl_id"],
                    row["created_account_move_id"],
                )
                for row in created_rows
            ],
        )

    def _apply_price_updates(self, price_updates):
        for row in price_updates:
            product = (
                self.env["product.product"]
                .browse(row["product_id"])
                .with_company(row["company_id"])
                .with_context(disable_auto_svl=True)
            )
            product.standard_price = row["new_standard_price"]

    def _build_report(
        self,
        keys,
        plans,
        svl_updates,
        adjustments,
        price_updates,
        apply=False,
        backup_tables=None,
        created_adjustments=None,
    ):
        quant_qty_map = self._fetch_quant_qty_map(keys)
        verification = [
            self._summarize_key(company_id, product_id, quant_qty=quant_qty_map.get((company_id, product_id), 0.0))
            for company_id, product_id in keys
        ]
        needs_adjustment_account = any(row["needs_account_move"] for row in adjustments)
        return {
            "db": self.env.cr.dbname,
            "apply": apply,
            "target_count": len(keys),
            "svl_update_count": len(svl_updates),
            "adjustment_count": len(adjustments),
            "price_update_count": len(price_updates),
            "apply_requirements": {
                "adjustment_account_required": needs_adjustment_account,
            },
            "backup_tables": backup_tables or {},
            "plan": plans,
            "created_adjustments": created_adjustments or [],
            "verification": verification,
        }

    def _apply_known_quantity_fixes(self, stamp):
        patch_rows = []
        forced_keys = set()
        table_name = None

        for patch in self._KNOWN_QUANTITY_FIXES:
            products = self.env["product.product"].with_context(active_test=False).search(
                [("default_code", "=", patch["default_code"])]
            )
            if not products:
                continue

            self.env.cr.execute(
                """
                SELECT company_id, product_id
                FROM stock_valuation_layer
                WHERE product_id = ANY(%s)
                GROUP BY company_id, product_id
                ORDER BY company_id, product_id
                """,
                (products.ids,),
            )
            forced_keys.update((company_id, product_id) for company_id, product_id in self.env.cr.fetchall())

            self.env.cr.execute(
                """
                SELECT id, company_id, product_id, quantity, value
                FROM stock_valuation_layer
                WHERE product_id = ANY(%s)
                  AND description = %s
                ORDER BY create_date, id
                """,
                (products.ids, patch["description"]),
            )
            candidates = self.env.cr.fetchall()
            if not candidates:
                continue
            if len(candidates) != 1:
                raise UserError("Quantity fix for %s is ambiguous" % patch["default_code"])

            svl_id, company_id, product_id, current_quantity, current_value = candidates[0]
            self.env.cr.execute(
                """
                SELECT COALESCE(SUM(quantity), 0), COALESCE(SUM(value), 0)
                FROM stock_valuation_layer
                WHERE product_id = %s
                  AND company_id = %s
                  AND description = %s
                """,
                (product_id, company_id, patch["return_description"]),
            )
            return_qty_sum, return_value_sum = self.env.cr.fetchone()
            target_quantity = -(return_qty_sum or 0.0)
            target_value = -(return_value_sum or 0.0)
            if float_is_zero(target_quantity, precision_rounding=0.0001):
                raise UserError("Quantity fix for %s did not find return rows" % patch["default_code"])
            if abs((current_value or 0.0) - target_value) > 1e-9:
                raise UserError("Quantity fix for %s failed value validation" % patch["default_code"])
            if abs((current_quantity or 0.0) - target_quantity) <= 1e-9:
                continue

            if table_name is None:
                table_name = "x_svl_quantity_fix_%s" % stamp
                self.env.cr.execute(
                    """
                    CREATE TABLE %s (
                        svl_id integer PRIMARY KEY,
                        company_id integer,
                        product_id integer,
                        default_code varchar,
                        description text,
                        old_quantity numeric,
                        new_quantity numeric,
                        note text,
                        backup_at timestamp without time zone
                    )
                    """
                    % table_name
                )

            self.env.cr.execute(
                f"""
                INSERT INTO {table_name} (
                    svl_id,
                    company_id,
                    product_id,
                    default_code,
                    description,
                    old_quantity,
                    new_quantity,
                    note,
                    backup_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
                """,
                (
                    svl_id,
                    company_id,
                    product_id,
                    patch["default_code"],
                    patch["description"],
                    current_quantity,
                    target_quantity,
                    patch["note"],
                ),
            )
            self.env.cr.execute(
                """
                UPDATE stock_valuation_layer
                SET quantity = %s,
                    write_date = now(),
                    write_uid = %s
                WHERE id = %s
                """,
                (target_quantity, SUPERUSER_ID, svl_id),
            )
            patch_rows.append(
                {
                    "svl_id": svl_id,
                    "company_id": company_id,
                    "product_id": product_id,
                    "default_code": patch["default_code"],
                    "old_quantity": current_quantity,
                    "new_quantity": target_quantity,
                    "description": patch["description"],
                }
            )

        if patch_rows:
            _logger.warning(
                "Applied known SVL quantity fixes: %s",
                json.dumps(patch_rows, ensure_ascii=False, default=str),
            )
        return {"rows": patch_rows, "backup_table": table_name}, forced_keys
