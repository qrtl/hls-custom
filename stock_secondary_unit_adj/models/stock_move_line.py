# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # Making secondary_uom_id a related field to move_id.secondary_uom_id would be
    # simpler, however that would make the design less flexible in case the possibility
    # of changing the secondary unit at line level comes out in the future.
    secondary_uom_id = fields.Many2one(
        default=lambda self: self._get_secondary_uom_default(),
    )

    @api.model
    def _get_secondary_uom_default(self):
        secondary_uom_id = self._context.get("secondary_uom_id")
        secondary_uom = self.env["product.secondary.unit"].browse(secondary_uom_id)
        return secondary_uom
