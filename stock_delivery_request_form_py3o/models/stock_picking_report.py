# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class StockPickingReport(models.TransientModel):
    _name = 'stock.picking.report'

    line_ids = fields.One2many(
        'stock.picking.report.line',
        inverse_name='report_id',
    )
    company_id = fields.Many2one('res.company')
    report_date = fields.Date(string='Report Date')
    user_id = fields.Many2one('res.users', string='Responsible person')
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
    )

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return _('Stock Report (%s - %s)' % (
            self.partner_id.name, fields.Date.to_string(self.report_date)))

    def _create_delivery_request_form(self, picking_ids, report_date, user_id, partner_id):
        report = self.create({
            'company_id': self.env.user.company_id.id,
            'report_date': report_date,
            'user_id': user_id.id,
            'partner_id': partner_id.id,
        })
        self.env['stock.picking.report.line']._create_delivery_request_form_lines(
            report, picking_ids)
        return report.id


class StockPickingReportLine(models.TransientModel):
    _name = 'stock.picking.report.line'

    report_id = fields.Many2one(
        'stock.picking.report',
    )
    move_id = fields.Many2one(
        'stock.move',
    )

    def _create_delivery_request_form_lines(self, report, picking_ids):
        for picking in picking_ids:
            for move in picking.move_line_ids:
                self.create({
                    'report_id': report.id,
                    'move_id': move.id,
                })
