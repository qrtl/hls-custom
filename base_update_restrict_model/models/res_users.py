# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    restrict_update_permit = fields.Boolean(
        "Update Permit", help="Set to true and the user can update restricted model."
    )

    @api.multi
    def toggle_restrict_update_permit(self):
        for record in self:
            record.restrict_update_permit = not record.restrict_update_permit
