# Copyright 2021 Quartile.co
#   (http://www.quartile.co)

from odoo import fields, models


class DateRange(models.Model):
    _inherit = "date.range"

    valuation_date = fields.Datetime(
        string="Inventory Valuate Date",
        help="Set the date that is intended to be used"
        "for showing the inventory at date.",
    )
