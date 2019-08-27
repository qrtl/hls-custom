# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        if self.model == 'account.invoice' and res_ids:
            py3o_report = self.env.ref(
                'account_invoice_report_hls.account_invoice_jp')
            return py3o_report.render_py3o(res_ids, data=data)
        return super(IrActionsReport, self).render_qweb_pdf(
            res_ids, data=data)
