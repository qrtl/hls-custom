# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DateRange(models.Model):
    _inherit = "date.range"

    valuation_date = fields.Datetime(
        string="Inventory Valuate Date",
        help="Set the date that is intended to be used"
        "for showing the inventory at date.",
    )
