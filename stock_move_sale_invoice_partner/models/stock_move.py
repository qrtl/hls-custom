# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_order_partner_id = fields.Many2one(
        related="sale_line_id.order_id.partner_id", string="Sales Order Customer",
    )
    invoice_partner_id = fields.Many2one(
        "res.partner",
        compute="_get_invoice_partner_id",
        store=True,
        string="Invoice Customer",
    )

    @api.multi
    @api.depends(
        "sale_line_id",
        "sale_line_id.order_id.partner_invoice_id",
        "sale_line_id.order_id.invoice_ids.partner_id",
    )
    def _get_invoice_partner_id(self):
        for move in self:
            if move.sale_line_id:
                move.invoice_partner_id = move.sale_line_id.order_id.partner_invoice_id
                invoices = move.sale_line_id.order_id.invoice_ids.filtered(
                    lambda s: s.state != "cancel"
                )
                if invoices:
                    move.invoice_partner_id = invoices[0].partner_id
