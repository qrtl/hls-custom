# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_qty_totals(self):
        """Return aggregated quantity totals grouped by unit.

        Returns a dict with 'primary' and 'secondary' recordsets of
        purchase.order.qty.total (in-memory .new() records) to support
        t-field rendering with report_qweb_field_option.
        """
        self.ensure_one()
        QtyTotal = self.env["purchase.order.qty.total"]
        primary_totals = {}
        secondary_totals = {}
        for line in self.order_line.filtered(lambda x: not x.display_type):
            uom = line.product_uom
            primary_totals.setdefault(uom, 0.0)
            primary_totals[uom] += line.product_qty
            if line.secondary_uom_id:
                sec_unit = line.secondary_uom_id
                secondary_totals.setdefault(sec_unit, 0.0)
                secondary_totals[sec_unit] += line.secondary_uom_qty
        primary_records = QtyTotal
        for uom, qty in primary_totals.items():
            primary_records |= QtyTotal.new(
                {"order_id": self.id, "qty": qty, "uom_id": uom.id}
            )
        secondary_records = QtyTotal
        for sec_unit, qty in secondary_totals.items():
            secondary_records |= QtyTotal.new(
                {
                    "order_id": self.id,
                    "qty": qty,
                    "uom_id": sec_unit.uom_id.id,
                }
            )
        return {"primary": primary_records, "secondary": secondary_records}
