from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    eta_date = fields.Char("Estimated Time of Arrival(ETA)")
    etd_date = fields.Char("Estimated Time of Departure(ETD)")
    quantity_total = fields.Float("Total Quantity", compute="_compute_quantity_total")

    @api.onchange("order_line")
    def _compute_quantity_total(self):
        qty_total = 0
        for pol in self.order_line:
            qty_total += pol.product_qty
        self.quantity_total = qty_total
