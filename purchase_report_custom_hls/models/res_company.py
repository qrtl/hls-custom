# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_representative = fields.Char("Company Representative", translate=True,)
    rep_signature = fields.Binary("Representative Signature", attachment=True)
