# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    purchase_address = fields.Text(
        "Purchase Address", help="Address for print purchase report."
    )
    company_representative = fields.Char()
    rep_signature = fields.Binary("Representative Signature", attachment=True)
