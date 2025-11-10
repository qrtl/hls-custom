# Copyright 2020-2022 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class StockLot(models.Model):
    _inherit = "stock.lot"

    removal_dt_date = fields.Date(
        compute="_compute_removal_dt_date",
        store=True,
        copy=False,
    )

    @api.depends("removal_date")
    def _compute_removal_dt_date(self):
        # Apply company's timezone if available.
        tz = self.env.user.company_id.partner_id.tz or "Japan"
        for lot in self.with_context(tz=tz).filtered("removal_date"):
            lot.removal_dt_date = fields.Datetime.context_timestamp(
                lot, lot.removal_date
            ).date()

    @api.depends("name", "removal_dt_date")
    def _compute_display_name(self):
        super()._compute_display_name()
        for lot in self.filtered("removal_dt_date"):
            date_str = lot.removal_dt_date.strftime("%Y/%m/%d")
            lot.display_name = f"[{date_str}] {lot.name}"
        return

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = expression.AND(
            [
                args,
                [
                    "|",
                    ("removal_dt_date", operator, name.replace("/", "-")),
                    ("name", operator, name),
                ],
            ]
        )
        records = self.search(domain, limit=limit)
        return [(rec.id, rec.display_name or "") for rec in records]
