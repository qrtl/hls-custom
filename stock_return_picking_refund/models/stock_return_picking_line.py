# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    to_refund = fields.Boolean(default=True)
