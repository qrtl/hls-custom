# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_price_discrepancy = fields.Boolean(
        compute="_compute_has_price_discrepancy", store=True
    )

    @api.depends(
        "order_line", "order_line.price_unit", "order_line.price_unit_pricelist"
    )
    def _compute_has_price_discrepancy(self):
        for order in self:
            for line in order.order_line:
                if line.product_id.type == "service":
                    continue
                if line.price_unit != line.price_unit_pricelist:
                    order.has_price_discrepancy = True
                    break
