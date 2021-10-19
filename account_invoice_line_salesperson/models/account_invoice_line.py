# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    user_id = fields.Many2one(
        "res.users", "Sales Person", readonly=True, compute="_compute_user_id",
    )

    @api.multi
    def _compute_user_id(self):
        user_list = []
        for line in self:
            if line.sale_line_ids:
                user_list.append(
                    sl.user_id for sl in line.sale_line_ids.mapped("order_id")
                )
        if user_list:
            line.user_id = user_list[0]
