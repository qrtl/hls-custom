# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def _create_picking(self):
        super(PurchaseOrder, self)._create_picking()
        for order in self:
            pickings = order.picking_ids.filtered(
                lambda x: x.state not in ("done", "cancel")
            )
            move_lines = pickings.mapped("move_line_ids").filtered(
                lambda x: x.product_id.tracking != "none"
            )
            move_lines.unlink()
        return True
