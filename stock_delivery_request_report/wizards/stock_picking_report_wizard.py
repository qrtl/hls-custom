# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPickingReportWizard(models.TransientModel):
    _name = 'stock.picking.report.wizard'

    report_date = fields.Date(
        string='Report Date',
        required=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsible person',
        required=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
    )

    def print_delivery_request_form(self):
        context = dict(self.env.context)
        picking_ids = self.env['stock.picking'].browse(
            context.get('picking_ids'))
        report_id = self.env['stock.picking.report']._create_delivery_request_form(
            picking_ids, self.report_date, self.user_id, self.partner_id)
        return self.env.ref('stock_delivery_request_report.delivery_request_form').report_action([report_id])
