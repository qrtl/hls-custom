# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    estimated_time_arrival = fields.Char("Estimated Time of Arrival(ETA)")
    estimated_time_departure = fields.Char("Estimated Time of Departure(ETD)")
