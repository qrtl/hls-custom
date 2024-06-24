# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    account_invoice_report = fields.Many2one(
        "ir.actions.report",
        help="This report will be used as a template in the customer portal "
        "view of the invoice.",
    )
