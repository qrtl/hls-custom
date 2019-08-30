# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class InvoiceDeliveryReport(models.TransientModel):
    _name = 'invoice.delivery.report'

    invoice_id = fields.Many2one('account.invoice')
    line_ids = fields.One2many(
        'invoice.delivery.report.line',
        inverse_name='report_id',
    )

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return _('Invoice (%s)' % (self.invoice_id.number))

    def _create_invoice_delivery_report(self, invoice):
        report = self.create({
            'invoice_id': invoice.id,
        })
        self.env['invoice.delivery.report.line']._create_invoice_delivery_report_lines(
            report, invoice.invoice_line_ids)
        return report.id


class InvoiceDeliveryReportLine(models.TransientModel):
    _name = 'invoice.delivery.report.line'

    report_id = fields.Many2one(
        'invoice.delivery.report',
    )
    move_id = fields.Many2one(
        'stock.move',
    )
    report_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
    )
    report_uom = fields.Char()
    # picking_id = fields.Many2one(
    #     related='move_id.picking_id',
    # )
    # partner_id = fields.Many2one(
    #     related='picking_id.partner_id',
    # )

    def _create_invoice_delivery_report_lines(self, report, invoice_line_ids):
        for il in invoice_line_ids.filtered(lambda x: x.product_id.type != 'service'):
            for sl in il.sale_line_ids:
                #FIXME add date range to the domain
                moves = self.env['stock.move'].search([
                    ('sale_line_id', '=', sl.id),
                    ('state', '=', 'done'),
                    ])
                if moves:
                    report_uom == ''
                    factor = 0.0
                    rounding_factor = 0.0
                    if sl.secondary_uom_id:
                        report_uom = sl.secondary_uom_id.name
                        factor = sl.secondary_uom_id.factor * sl.product_uom.factor
                        rounding_factor = sl.secondary_uom_id.uom_id.factor
                    else:
                        report_uom = sl.product_uom.name
                        factor = sl.product_uom.factor
                        rounding_factor = sl.product_uom.factor
                    for move in moves:
                        report_qty = float_round(
                            move.quantity_done / (factor or 1.0),
                            precision_rounding=rounding_factor
                        )
                        self.create({
                            'report_id': report.id,
                            'move_id': move.id,
                            'report_qty': report_qty,
                            'report_uom': report_uom,
                        })
