# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    restrict_update_permit = fields.Boolean(
        "Update Permit", help="Set True Means This User can update restricted model."
    )

    @api.multi
    def set_restrict_update_permit(self):
        self.write({"restrict_update_permit": True})

    @api.multi
    def unset_restrict_update_permit(self):
        self.write({"restrict_update_permit": False})
