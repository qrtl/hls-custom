# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.tools.float_utils import float_round


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    secondary_uom_qty = fields.Float(
        string='Secondary Qty',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_product_secondary_uom_qty',
        store=True,
    )
    secondary_uom_id = fields.Many2one(
        # comodel_name='product.secondary.unit',
        related='product_id.stock_secondary_uom_id',
        string='Secondary UoM',
    )
    # product_uom_po_id = fields.Many2one(
    #     'uom.uom', 'Purchase Unit of Measure',
    #     readonly=True,
    #     related='product_id.uom_po_id',
    # )
    # product_uom_po_qty = fields.Float(
    #     'Quantity in Purchase UoM',
    #     compute='_compute_product_uom_po_qty',
    #     store=True,
    # )

    @api.multi
    @api.depends('quantity', 'product_id.stock_secondary_uom_id')
    def _compute_product_secondary_uom_qty(self):
        for quant in self:
            if quant.product_id.stock_secondary_uom_id:
                uom = quant.product_uom_id
                factor = quant.product_id.stock_secondary_uom_id * uom.factor
                quant.secondary_uom_qty = float_round(
                    quant.quantity / (factor or 1.0),
                    precision_rounding=quant.product_id.secondary_uom_id.uom_id.factor
                )
