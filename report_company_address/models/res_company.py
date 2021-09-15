# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_name_address = fields.Html(
        "Company Name & Address",
        help="Company name and address that should show in report header when "
        "set. To reset the value, please update the source and "
        "translations strings of the translation record.",
        translate=True,
        sanitize=False,
    )
