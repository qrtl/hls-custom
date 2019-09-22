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
        self.env['invoice.delivery.report.line'].\
            _create_invoice_delivery_report_lines(report,
                                                  invoice.invoice_line_ids,
                                                  invoice.date_from,
                                                  invoice.date_to)
        return report.id


class InvoiceDeliveryReportLine(models.TransientModel):
    _name = 'invoice.delivery.report.line'

    report_id = fields.Many2one(
        'invoice.delivery.report',
    )
    move_id = fields.Many2one(
        'stock.move',
    )
    sale_line_id = fields.Many2one(
        'sale.order.line',
    )
    secondary_uom_id = fields.Many2one(
        'product.secondary.unit',
    )
    product_uom = fields.Many2one(
        'uom.uom',
    )
    move_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
    )
    secondary_qty = fields.Float(
        compute='_compute_secondary_qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    price_subtotal = fields.Float(
        compute='_compute_price_subtotal',
        digits=dp.get_precision('Product Price'),
    )

    def _create_invoice_delivery_report_lines(self, report, invoice_line_ids,
                                              date_from, date_to):
        for il in invoice_line_ids.filtered(
            lambda x: x.product_id.type != 'service').sorted(
                key=lambda r: r.sale_order_name or ''):
            for sl in il.sale_line_ids:
                moves = self.env['stock.move'].search([
                    ('sale_line_id', '=', sl.id),
                    ('state', '=', 'done'),
                    ('date_actual', '>=', date_from),
                    ('date_actual', '<=', date_to),
                ]).sorted(key=lambda m: m.date_actual)
                for move in moves:
                    move_qty = move.quantity_done * -1 \
                        if move.picking_code == 'incoming' \
                            else move.quantity_done
                    self.create({
                        'report_id': report.id,
                        'move_id': move.id,
                        'sale_line_id': sl.id,
                        'secondary_uom_id': sl.secondary_uom_id.id if \
                            sl.secondary_uom_id else False,
                        'move_qty': move_qty,
                        'product_uom': move.product_uom.id,
                    })

    @api.multi
    def _compute_secondary_qty(self):
        for line in self.filtered(lambda x: x.secondary_uom_id):
            factor = line.secondary_uom_id.factor * \
                line.product_uom.factor
            line.secondary_qty = float_round(
                line.move_qty / (factor or 1.0),
                precision_rounding=line.secondary_uom_id.uom_id.rounding
            )

    @api.multi
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.sale_line_id.price_unit * line.move_qty
