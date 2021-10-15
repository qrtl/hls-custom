# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    user_id = fields.Many2one(
        "res.users","Sales Person", index=True, readonly=True, compute="_compute_user_id"
    )

    @api.model
    def _compute_user_id(self):
        if not self.origin:
            self.user_id = self.create_uid
            return
        else: 
            for line in self:
                if line.sale_line_ids:
                    first_sale_order = line.sale_line_ids[1]
                    so_user_id = first_sale_order.user_id
                    line.user_id = so_user_id
