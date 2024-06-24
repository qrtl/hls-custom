# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    customer_invoice_portal_report = fields.Many2one(
        "ir.actions.report",
        domain="[('model', '=', 'account.invoice')]",
        help="This report template will be used in the customer portal to "
        "show the customer invoice.",
    )
