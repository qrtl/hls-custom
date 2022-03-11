# Copyright 2018 Tecnativa - Sergio Teruel
# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_round


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    secondary_uom_qty_done = fields.Float(
        "Secondary Done",
        default=0.0,
        digits=dp.get_precision("Product Unit of Measure"),
        copy=False,
    )

    @api.onchange("secondary_uom_id", "secondary_uom_qty_done")
    def _onchange_secondary_uom(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.product_uom_id.factor
        qty = float_round(
            self.secondary_uom_qty_done * factor,
            precision_rounding=self.product_uom_id.rounding,
        )
        if (
            float_compare(
                self.qty_done, qty, precision_rounding=self.product_uom_id.rounding
            )
            != 0
        ):
            self.qty_done = qty

    @api.onchange("qty_done")
    def _onchange_qty_done(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.product_uom_id.factor
        qty = float_round(
            self.qty_done / (factor or 1.0),
            precision_rounding=self.secondary_uom_id.uom_id.rounding,
        )
        if (
            float_compare(
                self.secondary_uom_qty_done,
                qty,
                precision_rounding=self.secondary_uom_id.uom_id.rounding,
            )
            != 0
        ):
            self.secondary_uom_qty_done = qty
