# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        related_partner_ids = []
        if self.partner_id:
            partners = self.env['res.partner'].search([
                ('commercial_partner_id', '=',
                 self.partner_id.commercial_partner_id.id)
            ])
            related_partner_ids.append(('id', 'in', partners.ids))
        return {
            'domain': {
                'partner_invoice_id': related_partner_ids,
                'partner_shipping_id': related_partner_ids,
            }
        }

    @api.onchange('partner_shipping_id')
    def _onchange_partner_shipping_id(self):
        if self.partner_shipping_id and \
                self.partner_shipping_id.invoice_partner_id:
            self.partner_invoice_id = \
                self.partner_shipping_id.invoice_partner_id
