# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountBilling(models.Model):
    _inherit = "account.billing"

    use_company_invoice = fields.Boolean(
        compute="_compute_use_company_invoice", store=True, readonly=False
    )
    invoice_send_method = fields.Selection(
        [
            ("post", "Post"),
            ("email", "Email"),
            ("do_not_send", "Do Not Send"),
            ("others", "Others"),
        ],
        compute="_compute_use_company_invoice",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id")
    def _compute_use_company_invoice(self):
        for rec in self:
            rec.use_company_invoice = rec.partner_id.use_company_invoice
            rec.invoice_send_method = rec.partner_id.invoice_send_method
