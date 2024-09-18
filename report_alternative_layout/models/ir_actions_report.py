# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Report(models.Model):
    _inherit = "ir.actions.report"

    show_commercial_partner = fields.Boolean(
        help="If selected, "
        "the commercial partner of the document partner will show "
        "in the report output (instead of the document partner)."
    )

    def _get_partner_id(self, xmlid, doc):
        doc.ensure_one()
        report = self._get_report_from_name(xmlid)
        if report.show_commercial_partner:
            return doc.partner_id.commercial_partner_id
        return doc.partner_id
