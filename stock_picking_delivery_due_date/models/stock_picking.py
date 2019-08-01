# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_due_date = fields.Datetime(
        'Delivery Due Date',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="The date the customer is expected to receive the delivery."
    )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
        submenu=False):
        if view_type == 'tree':
            pick_type_id = self._context.get('default_picking_type_id')
            if not pick_type_id or pick_type_id and \
                    self.env['stock.picking.type'].browse(
                        [pick_type_id]).code in 'outgoing':
                view_id = self.env.ref(
                    'stock_picking_delivery_due_date.vpicktree_outgoing').id
        return super(StockPicking, self).fields_view_get(view_id=view_id,
            view_type=view_type, toolbar=toolbar, submenu=submenu)
