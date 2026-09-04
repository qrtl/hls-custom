# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    end_customer = fields.Char(
        help="E.g. the customer beyond a trading company or wholesaler, such "
        "as a restaurant or supermarket."
    )
