# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def delivery_request_form(self):
        return {
            'name': _('Delivery Request Form'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.move.report.wizard',
            'view_id': self.env.ref('stock_delivery_request_form_py3o.stock_move_report_wizard').id,
            'type': 'ir.actions.act_window',
            'context': {
                'move_ids': self.env.context.get('active_id')
            },
            'target': 'new',
        }
