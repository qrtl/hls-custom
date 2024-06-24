# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortal(CustomerPortal):
    def _show_report(self, model, report_type, report_ref, download=False):
        invoice_report = request.env.user.company_id.account_invoice_report
        if model._name == "account.invoice" and invoice_report:
            external_id = invoice_report.get_external_id()
            report_ref = external_id.get(invoice_report.id)
        return super()._show_report(model, report_type, report_ref, download)
