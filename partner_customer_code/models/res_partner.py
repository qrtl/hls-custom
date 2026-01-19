# Copyright 2021 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_code = fields.Char(
        copy=False, help="Intended to be passed to the external accounting system."
    )

    _sql_constraints = [
        (
            "customer_code_uniq",
            "UNIQUE(customer_code)",
            "Customer Code must be unique.  Please enter another code.",
        )
    ]
