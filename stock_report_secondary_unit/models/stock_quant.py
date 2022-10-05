# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class StockQuant(models.Model):
    _inherit = "stock.quant"

    secondary_uom_qty = fields.Float(
        string="Secondary Qty",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_product_secondary_uom_qty",
        store=True,
    )
    secondary_uom_id = fields.Many2one(
        related="product_id.stock_secondary_uom_id",
        string="Secondary UoM",
    )

    @api.multi
    @api.depends("quantity", "product_id.stock_secondary_uom_id")
    def _compute_product_secondary_uom_qty(self):
        for quant in self.filtered(lambda x: x.product_id.stock_secondary_uom_id):
            uom = quant.product_uom_id
            secondary_uom = quant.product_id.stock_secondary_uom_id
            factor = secondary_uom.factor * uom.factor
            quant.secondary_uom_qty = float_round(
                quant.quantity / (factor or 1.0),
                precision_rounding=secondary_uom.uom_id.rounding,
            )
