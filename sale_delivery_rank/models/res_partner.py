# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_rank = fields.Selection(
        [("a", "A"), ("b", "B"), ("c", "C")],
        help="Rank assigned to a delivery destination. ",
    )
