# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Report(models.Model):
    _inherit = "ir.actions.report"

    apply_alternative_layout = fields.Boolean(
        help="If selected, the alternative layout will be applied in the printed "
        "report.",
    )
    show_commercial_partner = fields.Boolean(
        help="If selected, the commercial partner of the document partner will show "
        "in the report output (instead of the document partner)."
    )

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        if self.apply_alternative_layout:
            self = self.with_context(apply_alternative_layout=True)
        return super().render_qweb_pdf(res_ids, data)

    def _get_partner(self, xmlid, partner):
        report = self._get_report_from_name(xmlid)
        if report.show_commercial_partner:
            return partner.commercial_partner_id
        return partner
