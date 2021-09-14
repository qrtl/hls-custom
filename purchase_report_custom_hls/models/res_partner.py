# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    customer_incoterm_place = fields.Char(
        "Default Incoterm Place",
        help="The default incoterm place for purchase report.",
    )
