# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    commercial_partner_id = fields.Many2one(
        related="partner_id.commercial_partner_id",
        store=True,
        readonly=True,
    )

    @api.onchange("partner_shipping_id")
    def _onchange_partner_shipping_id(self):
        res = super(SaleOrder, self)._onchange_partner_shipping_id()
        if self.partner_shipping_id and self.partner_shipping_id.invoice_partner_id:
            self.partner_invoice_id = self.partner_shipping_id.invoice_partner_id
        return res
