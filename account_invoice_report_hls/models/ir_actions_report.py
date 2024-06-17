# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        if self.report_name == "account_invoice_report_hls.invoice_delivery":
            if not res_ids:
                res_ids = self.env.context.get("active_ids")
            invoices = self.env["account.invoice"].browse(res_ids)
            invoices._create_invoice_delivery_report()
        return super(IrActionsReport, self).render_qweb_pdf(res_ids, data)
