# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    secondary_unit_price = fields.Float(
        'Secondary Unit Price', 
        digits=dp.get_precision('Product Price')
    )

    @api.onchange('secondary_unit_price', 'price_unit')
    def onchange_unit_price(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * \
            self.product_uom.factor
        self.price_unit = self.secondary_unit_price / factor

    @api.onchange('product_id')
    def product_id_change(self):
        super(SaleOrderLine, self).product_id_change()
        self.secondary_unit_price = 0
        return

    @api.onchange('secondary_uom_id')
    def onchange_secondary_uom(self):
        super(SaleOrderLine, self).onchange_secondary_uom()
        if not self.secondary_uom_id:
            self.secondary_unit_price = 0
            return
