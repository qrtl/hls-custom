# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    input_secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Input Unit",
    )
    input_secondary_qty = fields.Float(
        string="Input Qty",
        digits="Product Unit of Measure",
        compute="_compute_input_secondary_qty",
        store=True,
        readonly=False,
    )

    @api.depends(
        "product_id", "product_uom_qty", "product_uom", "input_secondary_uom_id"
    )
    def _compute_input_secondary_qty(self):
        for line in self:
            uom = line.input_secondary_uom_id
            if not uom or uom.dependency_type == "independent":
                line.input_secondary_qty = 0.0
                continue
            line.input_secondary_qty = float_round(
                line._secondary_base_qty() / (uom.factor or 1.0),
                precision_rounding=uom.uom_id.rounding,
            )

    def _secondary_base_qty(self):
        self.ensure_one()
        qty = self.product_uom_qty
        uom_line = self.product_uom
        uom_product = self.product_id.uom_id
        if uom_line and uom_product and uom_line != uom_product:
            qty = uom_line._compute_quantity(qty, uom_product)
        return qty

    @api.onchange("input_secondary_qty")
    def _onchange_input_secondary(self):
        uom = self.input_secondary_uom_id
        if not uom or uom.dependency_type == "independent" or not self.product_id:
            return
        base_qty = self.input_secondary_qty * (uom.factor or 1.0)
        self.product_uom_qty = self.product_id.uom_id._compute_quantity(
            base_qty, self.product_uom
        )
        self.env.remove_to_compute(self._fields["input_secondary_qty"], self)
