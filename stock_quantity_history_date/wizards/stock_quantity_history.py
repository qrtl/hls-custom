# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockQuantityHistory(models.TransientModel):
    _inherit = "stock.quantity.history"

    date_range_id = fields.Many2one("date.range", string="Date Range")

    @api.onchange("date_range_id")
    def _onchange_date_range_id(self):
        for rec in self:
            if rec.date_range_id:
                rec.date = rec.date_range_id.valuation_date
