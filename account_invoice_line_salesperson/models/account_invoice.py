# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    user_id = fields.Many2one(
        "res.users", compute="_compute_salesperson", string="Salesperson", store=True
    )

    @api.multi
    @api.depends("sale_line_ids.order_id.user_id", "invoice_id.user_id")
    def _compute_salesperson(self):
        for line in self:
            if line.invoice_type not in ("out_invoice", "out_refund"):
                continue
            if line.sale_line_ids:
                line.user_id = line.sale_line_ids[0].order_id.user_id
                continue
            line.user_id = line.invoice_id.user_id
