# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    bl_date = fields.Date(string="B/L Date")

    @api.multi
    def _create_picking(self):
        res = super(PurchaseOrder, self)._create_picking()
        for order in self:
            if order.picking_ids:
                order.picking_ids.write({"bl_date": order.bl_date})
        return res
