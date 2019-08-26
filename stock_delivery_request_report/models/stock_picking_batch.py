# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    carrier_id  = fields.Many2one('delivery.carrier')