# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    use_company_invoice = fields.Boolean()
    invoice_send_method = fields.Selection(
        [
            ("post", "Post"),
            ("email", "Email"),
            ("do_not_send", "Do Not Send"),
            ("others", "Others"),
        ],
    )
