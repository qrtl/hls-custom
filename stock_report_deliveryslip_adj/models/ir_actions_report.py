# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields

class Report(models.Model):
    _inherit = 'ir.actions.report'

    commercial_partner = fields.Boolean()

    def _get_partner_id(self, doc):
        doc.ensure_one()
        # report = self._get_report_from_name("stock.report_deliveryslip")
        if report.commercial_partner:
            return doc.partner_id.commercial_partner_id
        else:
            return doc.partner_id
