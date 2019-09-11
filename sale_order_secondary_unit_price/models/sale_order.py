# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    secondary_unit_price = fields.Float(
        'Secondary Unit Price', 
        required=True, 
        digits=dp.get_precision('Product Price')
    )
