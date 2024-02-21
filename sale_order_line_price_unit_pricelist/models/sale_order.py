# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_price_matched = fields.Boolean(compute="_compute_is_price_matched", store=True)

    @api.onchange(
        "order_line", "order_line.price_unit", "order_line.price_unit_pricelist"
    )
    def _compute_is_price_matched(self):
        for order in self:
            order.is_price_matched = all(
                line.price_unit == line.price_unit_pricelist
                for line in order.order_line
            )
