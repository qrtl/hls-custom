# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    client_order_ref = fields.Char("Customer Order Ref")
