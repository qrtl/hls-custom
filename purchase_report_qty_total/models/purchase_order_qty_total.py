# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrderQtyTotal(models.Model):
    _name = "purchase.order.qty.total"
    _description = "Purchase Order Quantity Total"

    order_id = fields.Many2one("purchase.order")
    qty = fields.Float(digits="Product Unit of Measure")
    uom_id = fields.Many2one("uom.uom")
