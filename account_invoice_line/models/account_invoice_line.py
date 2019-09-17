# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    _order = "invoice_id,sequence desc,id desc"