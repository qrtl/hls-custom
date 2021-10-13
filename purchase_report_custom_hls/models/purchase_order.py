from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    estimated_time_arrival = fields.Char("Estimated Time of Arrival(ETA)")
    estimated_time_departure = fields.Char("Estimated Time of Departure(ETD)")
    quantity_total = fields.Float("Total Quantity", compute="_compute_quantity_total")

    @api.onchange("order_line")
    def _compute_quantity_total(self):
        qty_total = 0
        for pol in self.order_line:
            qty_total += pol.product_qty
        self.quantity_total = qty_total
