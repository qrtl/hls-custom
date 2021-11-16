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
        for line in self:
            order = self.env["sale.order"].search([("name", "=", self.sale_order_name)])
            if order:
                user = self.env["res.users"].search([("id", "=", order.user_id.id)])
        if user:
            line.user_id = user
        else:
            line.user_id = line.create_uid
