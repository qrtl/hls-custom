import ast
from odoo import fields, models


class StockQuantityHistory(models.TransientModel):
    _inherit = "stock.quantity.history"

    inventory_valuate_month = fields.Many2one(
        "date.range",
        readonly=True,
    )
