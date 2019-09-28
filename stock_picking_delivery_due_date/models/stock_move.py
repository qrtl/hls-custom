# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    date_delivered = fields.Date(
        'Delivered Date',
        related='picking_id.date_delivered',
        store=True,
    )

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        if self.sale_line_id:
            order = self.sale_line_id.order_id
            vals['delivery_due_date'] = order._get_due_date()
        return vals
