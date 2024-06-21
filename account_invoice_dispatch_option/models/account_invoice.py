# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    use_company_invoice = fields.Boolean()
    invoice_send_method = fields.Selection(
        [
            ("post", "Post"),
            ("email", "Email"),
            ("do_not_send", "Do Not Send"),
            ("others", "Others"),
        ],
    )

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        self.use_company_invoice = self.partner_id.use_company_invoice
        self.invoice_send_method = self.partner_id.invoice_send_method
        return super()._onchange_partner_id()
