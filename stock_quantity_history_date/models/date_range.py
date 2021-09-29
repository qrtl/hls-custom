# Copyright 2021 Quartile.co
#   (http://www.quartile.co)

from odoo import fields, models


class DateRange(models.Model):
    _inherit = "date.range"

    inventory_valuate_date = fields.Date(string="Inventory Valuate Date")
