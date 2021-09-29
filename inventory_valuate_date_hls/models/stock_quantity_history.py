# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    date_range_id = fields.Many2one("date.range", string="Date Range")
