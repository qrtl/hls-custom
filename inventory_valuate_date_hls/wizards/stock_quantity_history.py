from odoo import fields, models

class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    date_range = fields.Many2one('date.range', string="Date Range")
    inventory_valuate_date = fields.Date(string="Inventory Valuate Date", related='date_range.inventory_valuate_date', readonly=True, store=True)
