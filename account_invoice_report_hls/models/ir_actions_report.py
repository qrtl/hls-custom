# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @api.multi
    def render_qweb_pdf(self, res_id=None, data=None):
        if self.report_name == "account_invoice_report_hls.invoice_delivery":
            invoices = self.env["account.invoice"].browse(res_id)
            invoices._create_invoice_delivery_report()
        return super(IrActionsReport, self).render_qweb_pdf(res_id, data)
