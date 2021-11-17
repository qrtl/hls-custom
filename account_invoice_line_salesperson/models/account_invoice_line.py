# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    salesman_id = fields.Many2one(
        "res.users", "Sales Person", compute="_compute_salesman_id", store=True
    )

    @api.depends("sale_line_ids")
    def _compute_salesman_id(self):
        for line in self:
            if line.sale_line_ids:
                line.salesman_id = line.sale_line_ids[0].salesman_id
            else:
                line.salesman_id = line.invoice_id.user_id
