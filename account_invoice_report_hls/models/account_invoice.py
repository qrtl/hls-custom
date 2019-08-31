# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    monthly_invoice = fields.Boolean(
        'Monthly Invoice',
        default=True,
        help="If selected, shows the delivery details in the printed "
             "invoice.",
    )
    doc_title = fields.Char(
        'Doc Title',
        help="The value gets newly proposed when Invoice Date is changed."
    )
    date_range_id = fields.Many2one(
        'date.range',
        'Date Range',
        help="Select in case the invoice date does not fall into the target "
             "date range for the invoice."
    )
    date_from = fields.Date(
        'Date From',
    )
    date_to = fields.Date(
        'Date To',
    )
    picking_ids = fields.One2many(
        'stock.picking',
        string='Related Stock Pickings',
        inverse_name='invoice_id',
    )

    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        for inv in self:
            date = inv.date_invoice or fields.Date.from_string(
                fields.Date.context_today(self))
            # here we assume that all the invoices will be in Japanese
            inv.doc_title = str(date.month) + '月分'
            inv.date_from = date.replace(day=1)
            inv.date_to = inv.date_from + relativedelta(months=1, days=-1)

    @api.onchange('date_range_id')
    def onchange_date_range_id(self):
        if self.date_range_id:
            self.date_from = self.date_range_id.date_start
            self.date_to = self.date_range_id.date_end
