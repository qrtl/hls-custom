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

    @api.onchange('product_id')
    def product_id_change(self):
        self.secondary_unit_price = 0
        super(SaleOrderLine, self).product_id_change()

    @api.onchange('secondary_uom_id', 'secondary_unit_price')
    def onchange_secondary_price(self):
        if not self.secondary_uom_id:
            self.secondary_unit_price = 0
            return
        if self.secondary_unit_price:
            factor = self.secondary_uom_id.factor * self.product_uom.factor
            self.price_unit = self.secondary_unit_price / factor

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        """ secondary unit price should not be updated unless the field
            already keeps a value. i.e. secondary unit price will show on
            printed invoice in case it is not 0.0.
        """
        if not (self.secondary_uom_id and self.secondary_unit_price):
            return
        factor = self.secondary_uom_id.factor * self.product_uom.factor
        self.secondary_unit_price = self.price_unit * factor

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        """ extending the standard method to always respect the pricing
            based on the secondary unit price if it is set.
            i.e. standard method recomputes unit price irrespective of
            secondary unit price, so we need to override it.
        """
        super(SaleOrderLine, self).product_uom_change()
        self.onchange_secondary_price()
