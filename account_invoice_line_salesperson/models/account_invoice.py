# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _compute_user_id(self):
        for line in self.invoice_line_ids:
            if line.sale_line_ids:
                order = line.sale_line_ids.mapped("order_id")
                line.user_id = order.user_id
            else:
                line.user_id = line.create_uid
