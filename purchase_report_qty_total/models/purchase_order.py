# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_qty_totals(self):
        """Return aggregated quantity totals grouped by unit.

        Returns a recordset of purchase.order.qty.total (in-memory .new()
        records) where each record represents a primary UOM total with its
        paired secondary totals accessible via secondary_ids.
        """
        self.ensure_one()
        QtyTotal = self.env["purchase.order.qty.total"]
        uom_data = {}
        for line in self.order_line.filtered(lambda x: not x.display_type):
            uom = line.product_uom
            uom_data.setdefault(uom, {"qty": 0.0, "secondary": {}})
            uom_data[uom]["qty"] += line.product_qty
            if line.secondary_uom_id:
                sec_unit = line.secondary_uom_id
                uom_data[uom]["secondary"].setdefault(sec_unit, 0.0)
                uom_data[uom]["secondary"][sec_unit] += line.secondary_uom_qty
        records = QtyTotal
        for uom, data in uom_data.items():
            records |= QtyTotal.new(
                {
                    "order_id": self.id,
                    "qty": data["qty"],
                    "uom_id": uom.id,
                    "secondary_ids": [
                        Command.create({"qty": qty, "uom_id": sec_unit.uom_id.id})
                        for sec_unit, qty in data["secondary"].items()
                    ],
                }
            )
        return records
