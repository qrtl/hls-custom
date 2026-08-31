# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    end_customer = fields.Char(
        compute="_compute_end_customer",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id")
    def _compute_end_customer(self):
        for order in self:
            order.end_customer = order.partner_id.end_customer

    def _prepare_invoice(self):
        values = super()._prepare_invoice()
        values["end_customer"] = self.end_customer
        return values
