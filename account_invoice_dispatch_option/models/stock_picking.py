# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    use_company_invoice = fields.Boolean()
    invoice_send_method = fields.Selection(
        [
            ("post", "Post"),
            ("email", "Email"),
            ("do_not_send", "Do Not Send"),
            ("others", "Others"),
        ],
    )

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.partner_id:
            res.use_company_invoice = res.partner_id.use_company_invoice
            res.invoice_send_method = res.partner_id.invoice_send_method
        return res

    @api.multi
    def write(self, vals):
        partner_id = vals.get("partner_id")
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            vals.update(
                {
                    "use_company_invoice": partner.use_company_invoice,
                    "invoice_send_method": partner.invoice_send_method,
                }
            )
        return super(StockPicking, self).write(vals)
