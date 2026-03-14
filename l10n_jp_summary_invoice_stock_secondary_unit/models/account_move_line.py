# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    stock_secondary_uom_id = fields.Many2one(
        related="product_id.stock_secondary_uom_id",
    )
    stock_secondary_uom_qty = fields.Float(
        compute="_compute_stock_secondary_uom_qty",
        digits="Product Unit of Measure",
    )
    signed_stock_secondary_uom_qty = fields.Float(
        compute="_compute_signed_stock_secondary_uom_qty",
        digits="Product Unit of Measure",
    )

    @api.depends("quantity", "product_id")
    def _compute_stock_secondary_uom_qty(self):
        for line in self:
            stock_uom = line.stock_secondary_uom_id
            if not stock_uom:
                line.stock_secondary_uom_qty = 0.0
                continue
            qty = line.quantity
            uom_product = line.product_id.uom_id
            if line.product_uom_id != uom_product:
                qty = line.product_uom_id._compute_quantity(qty, uom_product)
            line.stock_secondary_uom_qty = float_round(
                qty / (stock_uom.factor or 1.0),
                precision_rounding=stock_uom.uom_id.rounding,
            )

    @api.depends("stock_secondary_uom_qty", "move_type")
    def _compute_signed_stock_secondary_uom_qty(self):
        for line in self:
            sign = -1 if line.move_type in ("out_refund", "in_refund") else 1
            line.signed_stock_secondary_uom_qty = line.stock_secondary_uom_qty * sign
