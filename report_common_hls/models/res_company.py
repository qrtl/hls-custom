# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_chop = fields.Binary(
        "Company Chop Image",
        attachment=True,
    )
    fax = fields.Char("Fax")
    rep_title = fields.Text(
        "Title of the Representative",
        translate=True,
        help="The input value is may show as the title of the representative"
        " in some of the printed documents.",
    )
    rep_signature = fields.Binary("Representative Signature", attachment=True)
