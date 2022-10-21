# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    """Override the method that compute a multiline description of this
    product, in the context of sales, to display/output product
    description (sale.order.line.name) without reference code.
    """

    _inherit = "product.product"

    def get_product_multiline_description_sale(self):
        name = self.name
        if self.description_sale:
            name += "\n" + self.description_sale
        return name
