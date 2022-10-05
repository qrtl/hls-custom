# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    eta_date = fields.Char(
        "ETA",
        help="Fill in your expected arrival date request(e.g. ASAP).",
    )
    etd_date = fields.Char(
        "ETD", help="Fill in your expected departure date request(e.g. ASAP)."
    )
    quantity_total = fields.Text(compute="_compute_qty_total")
    secondary_qty_total = fields.Text(
        "Secondary Quantity Total", compute="_compute_qty_total"
    )
    display_tax = fields.Boolean(
        "Display Tax",
        default=False,
        help="If checked, display tax in purchase order report.",
    )
    display_date_req = fields.Boolean(
        "Display Requested Date",
        default=False,
        help="If checked, display requested date in purchase order report.",
    )

    @api.model
    def _get_qty_total(self, qty_dict):
        if not qty_dict:
            return False
        # e.g. '400.0 kg'
        return "\n".join(str(v) + " " + k for k, v in qty_dict.items())

    def _compute_qty_total(self):
        for order in self:
            qty_dict = {}
            sec_qty_dict = {}
            for line in self.order_line:
                uom = line.product_uom
                if uom:
                    qty_dict.setdefault(uom.name, 0.0)
                    qty_dict[uom.name] += line.product_qty
                sec_uom = line.secondary_uom_id
                if sec_uom:
                    sec_qty_dict.setdefault(sec_uom.name, 0.0)
                    sec_qty_dict[sec_uom.name] += line.secondary_uom_qty
            order.quantity_total = self._get_qty_total(qty_dict)
            order.secondary_qty_total = self._get_qty_total(sec_qty_dict)
