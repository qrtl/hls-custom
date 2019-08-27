# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPickingReportWizard(models.TransientModel):
    _name = 'stock.picking.report.wizard'

    def print_delivery_request_form(self):
        context = dict(self.env.context)
        bps = self.env['stock.picking.batch'].browse(context.get('active_ids'))
        for bp in bps:
            report_id = self.env['stock.picking.report'].\
                _create_delivery_request_form(bp)
            return self.env.ref(
                'stock_delivery_request_report.delivery_request_form'
                ).report_action([report_id])
