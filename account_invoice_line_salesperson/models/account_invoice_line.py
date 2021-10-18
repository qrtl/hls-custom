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
        for line in self:
            first_so = line.sale_line_ids.mapped("order_id")[0]
            if not first_so:
                line.user_id = line.create_uid
            else:
                so_user_id = first_so.user_id
                line.user_id = so_user_id
                return
