# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_shipping_id")
    def _onchange_partner_shipping_id(self):
        res = super(SaleOrder, self)._onchange_partner_shipping_id()
        if self.partner_shipping_id:
            if self.partner_shipping_id.user_id:
                self.user_id = self.partner_shipping_id.user_id
            if self.partner_shipping_id.warehouse_id:
                self.warehouse_id = self.partner_shipping_id.warehouse_id
            self.carrier_id = self.partner_shipping_id.property_delivery_carrier_id.filtered('active')
        return res

    @api.onchange('partner_id')
    def onchange_partner_id_carrier_id(self):
        # if self.partner_id:
        #     self.carrier_id = self.partner_id.property_delivery_carrier_id.filtered('active')
        return
