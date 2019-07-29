# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockMoveReport(models.TransientModel):
    _name = 'stock.move.report'

    line_ids = fields.One2many(
        'stock.move.report.line',
        inverse_name='report_id',
    )
    company_id = fields.Many2one('res.company')
    report_date = fields.Date(string='Report Date')
    user_id = fields.Many2one('res.users', string='Responsible person')
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True
    )

    def _create_delivery_request_form(self, move_ids, report_date, user_id, partner_id):
        report = self.create({
            'company_id': self.env.user.company_id.id,
            'report_date': report_date,
            'user_id': user_id.id,
            'partner_id': partner_id.id,
        })
        self.env['stock.move.report.line']._create_delivery_request_form_lines(
            report, move_ids)
        return report.id


class StockMoveReportLine(models.TransientModel):
    _name = 'stock.move.report.line'

    report_id = fields.Many2one(
        'stock.move.report',
    )
    move_id = fields.Many2one(
        'stock.move',
    )

    def _create_delivery_request_form_lines(self, report, move_ids):
        for move in move_ids:
            self.create({
                'report_id': report.id,
                'move_id': move.id,
            })
