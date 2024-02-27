# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_delivery_slip_required = fields.Boolean()

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.partner_id:
            res.is_delivery_slip_required = res.partner_id.is_delivery_slip_required
        return res

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if vals.get("partner_id"):
            for rec in self:
                rec.is_delivery_slip_required = rec.partner_id.is_delivery_slip_required
        return res
