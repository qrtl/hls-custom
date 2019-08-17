# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import locale

from odoo import fields, models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    doc_title = fields.Char(
        'Doc Title',
        help="The value gets newly proposed when Invoice Date is changed."
    )

    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        # here we assume that all the invoices will be in Japanese
        for inv in self:
            date = inv.date_invoice or fields.Date.from_string(
                fields.Date.context_today(self))
            inv.doc_title = str(date.month) + '月分'
