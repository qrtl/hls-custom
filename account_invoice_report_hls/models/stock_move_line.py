# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    invoice_id = fields.Many2one(
        related='picking_id.invoice_id',
        string='Invoice',
        readonly=True,
    )
    invoice_line_id = fields.Many2one(
        'account.invoice.line',
        compute='_compute_invoice_fields',
    )
    price_subtotal = fields.Float(
        compute='_compute_invoice_fields',
        string='Subtotal',
        digits=dp.get_precision('Product Price'),
    )

    @api.multi
    def _compute_invoice_fields(self):
        for move_line in self:
            if move_line.invoice_id:
                invoice_line = move_line.invoice_id.invoice_line_ids.filtered(
                    lambda l: l.product_id == move_line.product_id
                )
                if invoice_line:
                    move_line.invoice_line_id = invoice_line[0]
                    move_line.price_subtotal = invoice_line[0].price_unit * move_line.qty_done
