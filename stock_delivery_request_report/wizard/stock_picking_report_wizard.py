# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPickingReportWizard(models.TransientModel):
    _name = 'stock.picking.report.wizard'

    # report_date = fields.Date(
    #     string='Report Date',
    #     required=True,
    #     default=fields.Date.context_today,
    # )
    # user_id = fields.Many2one(
    #     'res.users',
    #     string='Person in Charge',
    #     required=True,
    #     default=lambda self: self.env.user,
    # )
    # partner_id = fields.Many2one(
    #     'res.partner',
    #     string='Carrier',
    #     required=True,
    # )

    def print_delivery_request_form(self):
        context = dict(self.env.context)
        bp = self.env['stock.picking.batch'].browse(context.get('active_ids'))[0]
        report_id = self.env['stock.picking.report'].\
            _create_delivery_request_form(bp)
        # picking_ids = self.env['stock.picking'].browse(
        #     context.get('picking_ids'))
        # report_id = self.env['stock.picking.report'].\
        #     _create_delivery_request_form(
        #         picking_ids, self.report_date, self.user_id, self.partner_id)
        return self.env.ref(
            'stock_delivery_request_report.delivery_request_form'
            ).report_action([report_id])
