# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    update_restrict = fields.Boolean(
        'Update Restrict Model'
    )
