# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    carrier_id = fields.Many2one("delivery.carrier")
    ship_date = fields.Date(
        "Shipping Date",
        default=fields.Date.context_today,
        copy=False,
    )
    user_id = fields.Many2one(
        default=lambda self: self.env.user,
    )
    instruction = fields.Text()

    @api.onchange("carrier_id")
    def _onchange_carrier_id(self):
        self.instruction = (
            self.carrier_id.default_instruction if self.carrier_id else False
        )
