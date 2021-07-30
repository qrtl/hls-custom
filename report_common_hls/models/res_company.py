# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_chop = fields.Binary("Company Chop Image", attachment=True,)
    rep_signature = fields.Binary("Representative Signature", attachment=True,)
    ceo = fields.Char("Representative Director")
    fax = fields.Char("Fax")
