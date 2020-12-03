# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    date_delivered = fields.Date(
        "Delivered Date", related="picking_id.date_delivered", store=True
    )

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        if self.sale_line_id:
            order = self.sale_line_id.order_id
            vals["delivery_due_date"] = order._get_due_date()
        return vals
