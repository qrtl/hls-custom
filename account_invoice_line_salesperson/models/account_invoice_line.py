# Copyright 2021 Quartile Limited
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
            for sl in line.sale_line_ids:
                orders = self.env["sale.order"].search(
                    [("name", "=", sl.order_id.name)]
                )
                if orders:
                    for order in orders:
                        user = self.env["res.users"].search(
                            [("id", "=", order.user_id.id)]
                        )
                        user_list.append(user)
            if user_list:
                line.user_id = user_list[0]
            else:
                line.user_id = line.create_uid
