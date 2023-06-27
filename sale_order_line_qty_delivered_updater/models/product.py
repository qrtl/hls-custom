# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_amount_adj_product = fields.Boolean(
        related="product_tmpl_id.is_amount_adj_product",
        string="Amount Adjustment Product",
    )
