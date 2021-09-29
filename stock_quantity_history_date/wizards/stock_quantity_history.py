# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    date_range_id = fields.Many2one("date.range", string="Date Range")
    valuate_date = fields.Date(string="Inventory Valuate Date", compute="_compute_valuate_date")

    @api.onchange
    def _compute_valuate_date(self):
        for stock in self:
            if stock.date_range_id.inventory_valuate_date:
                stock.valuate_date = stock.date_range_id.inventory_valuate_date
