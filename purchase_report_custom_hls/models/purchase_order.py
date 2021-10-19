from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    eta_date = fields.Char("ETA")
    etd_date = fields.Char("ETD")
    quantity_total = fields.Float("Total Quantity", compute="_compute_quantity_total")

    @api.depends("order_line")
    def _compute_quantity_total(self):
        for order in self:
            order.quantity_total = sum([x.product_qty for x in order.order_line])
