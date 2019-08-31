# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    date_actual = fields.Date(
        'Actual Date',
        related='picking_id.date_actual',
        store=True,
    )
