# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_checked_line = fields.Boolean(
        string='Has Checked Line',
        compute='_compute_has_checked_line',
        store=True,
        help="Indicates that the order contains a line that has been checked "
             "for invoicing.",
    )

    @api.depends('order_line.line_checked')
    def _compute_has_checked_line(self):
        for order in self:
            if order.order_line.filtered(lambda x: x.line_checked):
                order.has_checked_line = True
            else:
                order.has_checked_line = False
