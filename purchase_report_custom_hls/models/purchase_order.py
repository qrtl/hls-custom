# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    eta_date = fields.Char(
        "ETA", help="Fill in your expected arrival date request(e.g. ASAP).",
    )
    etd_date = fields.Char(
        "ETD", help="Fill in your expected departure date request(e.g. ASAP)."
    )
    quantity_total = fields.Float("Total Quantity", compute="_compute_quantity_total")
    secondary_qty_total = fields.Float(
        "Total Secondary Quantity", compute="_compute_secondary_qty_total"
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

    @api.depends("order_line")
    def _compute_quantity_total(self):
        for order in self:
            order.quantity_total = sum([x.product_qty for x in order.order_line])

    @api.depends("order_line")
    def _compute_secondary_qty_total(self):
        for order in self:
            uom_list = order.order_line.mapped("secondary_uom_id.name")
            for uom in uom_list:
                order.secondary_qty_total = sum(
                    order.order_line.filtered(
                        lambda l: l.secondary_uom_id.uom_id == uom
                    ).mapped("secondary_uom_qty")
                )
