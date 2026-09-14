# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    alt_secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Alternative Secondary Unit",
    )
    alt_secondary_qty = fields.Float(
        digits="Product Unit of Measure",
        compute="_compute_alt_secondary_qty",
        inverse="_inverse_alt_secondary_qty",
        store=True,
        readonly=False,
    )

    def _convert_qty_to_alt_secondary_uom(self):
        self.ensure_one()
        uom = self.alt_secondary_uom_id
        qty = self.product_uom_qty
        uom_line = self.product_uom
        uom_product = self.product_id.uom_id
        if uom_line and uom_product and uom_line != uom_product:
            qty = uom_line._compute_quantity(qty, uom_product)
        return float_round(
            qty / (uom.factor or 1.0),
            precision_rounding=uom.uom_id.rounding,
        )

    @api.depends("product_id", "product_uom_qty", "product_uom", "alt_secondary_uom_id")
    def _compute_alt_secondary_qty(self):
        for line in self:
            uom = line.alt_secondary_uom_id
            if not uom or uom.dependency_type == "independent":
                line.alt_secondary_qty = 0.0
                continue
            line.alt_secondary_qty = line._convert_qty_to_alt_secondary_uom()

    def _apply_alt_secondary_qty(self):
        for line in self:
            uom = line.alt_secondary_uom_id
            if not uom or uom.dependency_type == "independent" or not line.product_id:
                continue
            base_qty = line.alt_secondary_qty * (uom.factor or 1.0)
            line.product_uom_qty = line.product_id.uom_id._compute_quantity(
                base_qty, line.product_uom
            )

    @api.onchange("alt_secondary_qty")
    def _onchange_alt_secondary_qty(self):
        self._apply_alt_secondary_qty()
        # Keep the value entered by the user: writing product_uom_qty above marks
        # this field to be recomputed from it.
        self.env.remove_to_compute(self._fields["alt_secondary_qty"], self)

    def _inverse_alt_secondary_qty(self):
        self._apply_alt_secondary_qty()
        # On create(), secondary_uom_qty is precomputed (and thus protected) before
        # this inverse updates product_uom_qty, so it would keep a stale value.
        self.env.add_to_compute(self._fields["secondary_uom_qty"], self)
