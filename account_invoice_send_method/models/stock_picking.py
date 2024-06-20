# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    use_company_invoice = fields.Boolean(
        related="partner_id.use_company_invoice", store=True
    )
    invoice_send_method = fields.Selection(
        related="partner_id.invoice_send_method", store=True
    )
