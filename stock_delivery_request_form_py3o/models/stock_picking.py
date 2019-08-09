# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    report_address = fields.Char(
        compute='_get_report_address',
    )

    @api.multi
    def _get_report_address(self):
        for picking in self:
            picking.report_address = picking.partner_id._display_address()

    @api.multi
    def delivery_request_form(self):
        picking_ids = self.browse(self.env.context.get('active_ids'))
        return {
            'name': _('Delivery Request Form'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking.report.wizard',
            'view_id': self.env.ref('stock_delivery_request_form_py3o.stock_picking_report_wizard').id,
            'type': 'ir.actions.act_window',
            'context': {
                'picking_ids': self.env.context.get('active_ids'),
            },
            'target': 'new',
        }
