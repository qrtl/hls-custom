# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    product_uom_po_id = fields.Many2one(
        "uom.uom",
        "Purchase Unit of Measure",
        readonly=True,
        related="product_id.uom_po_id",
    )
    product_uom_po_qty = fields.Float(
        "Quantity in Purchase UoM",
        compute="_compute_product_uom_po_qty",
        store=True,
    )

    @api.multi
    @api.depends("product_uom_qty", "product_id.uom_po_id")
    def _compute_product_uom_po_qty(self):
        for move in self:
            move.product_uom_po_qty = move.product_uom._compute_quantity(
                move.product_uom_qty, move.product_uom_po_id, round=False
            )
