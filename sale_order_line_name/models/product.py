# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    """ Override the method that compute a multiline description of this product, in the context of sales.
        In order to display/output product name without reference code.
    """
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        return self.name
