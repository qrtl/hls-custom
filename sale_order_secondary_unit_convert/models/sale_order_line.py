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
        inverse="_inverse_input_secondary_qty",
        store=True,
        readonly=False,
    )

    def _convert_qty_to_input_secondary_uom(self):
        self.ensure_one()
        uom = self.input_secondary_uom_id
        qty = self.product_uom_qty
        uom_line = self.product_uom
        uom_product = self.product_id.uom_id
        if uom_line and uom_product and uom_line != uom_product:
            qty = uom_line._compute_quantity(qty, uom_product)
        return float_round(
            qty / (uom.factor or 1.0),
            precision_rounding=uom.uom_id.rounding,
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
            line.input_secondary_qty = line._convert_qty_to_input_secondary_uom()

    def _inverse_input_secondary_qty(self):
        for line in self:
            uom = line.input_secondary_uom_id
            if not uom or uom.dependency_type == "independent" or not line.product_id:
                continue
            base_qty = line.input_secondary_qty * (uom.factor or 1.0)
            line.product_uom_qty = line.product_id.uom_id._compute_quantity(
                base_qty, line.product_uom
            )
            line.env.remove_to_compute(line._fields["input_secondary_qty"], line)
