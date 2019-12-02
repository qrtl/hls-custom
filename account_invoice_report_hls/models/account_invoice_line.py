# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    sale_order_name = fields.Char(
        "Sales Order Number", compute="_compute_sale_order_vals"
    )
    shipping_address_name = fields.Char(
        "Shipping Address Name", compute="_compute_sale_order_vals"
    )

    def _compute_sale_order_vals(self):
        for line in self:
            if line.sale_line_ids:
                line.sale_order_name = ", ".join(
                    [sl.order_id.name for sl in line.sale_line_ids]
                )
                line.shipping_address_name = ", ".join(
                    [
                        sl.order_id.partner_shipping_id.display_name or ""
                        for sl in line.sale_line_ids
                    ]
                )
