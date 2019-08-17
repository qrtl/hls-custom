# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round, float_compare


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    secondary_uom_qty = fields.Float(
        string='Secondary Qty',
        digits=dp.get_precision('Product Unit of Measure'),
        # compute='_compute_product_secondary_uom_qty',
        # store=True,
    )
    secondary_uom_id = fields.Many2one(
        'product.secondary.unit',
        # related='product_id.sale_secondary_uom_id',
        string='Secondary UoM',
        ondelete='restrict',
    )

    @api.onchange('secondary_uom_id', 'secondary_uom_qty')
    def onchange_secondary_uom(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.uom_id.factor
        qty = float_round(
            self.secondary_uom_qty * factor,
            precision_rounding=self.uom_id.rounding
        )
        if float_compare(
                self.quantity, qty,
                precision_rounding=self.uom_id.rounding) != 0:
            self.quantity = qty

    @api.onchange('quantity')
    def onchange_secondary_unit_product_uom_qty(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.uom_id.factor
        qty = float_round(
            self.quantity / (factor or 1.0),
            precision_rounding=self.secondary_uom_id.uom_id.rounding
        )
        if float_compare(
                self.secondary_uom_qty, qty,
                precision_rounding=self.secondary_uom_id.uom_id.rounding) != 0:
            self.secondary_uom_qty = qty

    @api.onchange('uom_id')
    def onchange_product_uom_for_secondary(self):
        if not self.secondary_uom_id:
            return
        factor = self.uom_id.factor * self.secondary_uom_id.factor
        qty = float_round(
            self.quantity / (factor or 1.0),
            precision_rounding=self.uom_id.rounding
        )
        if float_compare(
                self.secondary_uom_qty, qty,
                precision_rounding=self.uom_id.rounding) != 0:
            self.secondary_uom_qty = qty

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        If default sales secondary unit set on product, put on secondary
        quantity 1 for being the default quantity. We override this method,
        that is the one that sets by default 1 on the other quantity with that
        purpose.
        """
        res = super(AccountInvoiceLine, self)._onchange_product_id()
        self.secondary_uom_id = self.product_id.sale_secondary_uom_id
        if self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
            self.onchange_secondary_uom()
        return res
