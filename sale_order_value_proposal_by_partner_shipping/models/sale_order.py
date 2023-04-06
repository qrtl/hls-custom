# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_shipping_id")
    def _onchange_partner_shipping_id(self):
        res = super(SaleOrder, self)._onchange_partner_shipping_id()
        partner = self.partner_shipping_id
        if partner:
            if partner.user_id:
                self.user_id = partner.user_id
            if partner.warehouse_id:
                self.warehouse_id = partner.warehouse_id
            self.carrier_id = partner.property_delivery_carrier_id.filtered("active")
        return res
