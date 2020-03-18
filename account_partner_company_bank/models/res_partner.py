# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # bank_info = fields.Text('Bank Information')
    company_bank_id = fields.Many2one(
        "res.partner.bank",
        string="Remit-to Bank Account",
        help="Company's bank account which the customer should remit payments to.",
    )
