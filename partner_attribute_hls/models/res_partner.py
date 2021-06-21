# Copyright 2021 Quartile Limited

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_code = fields.Char(
        copy=False, help="Intended to be passed to the external accounting system."
    )
