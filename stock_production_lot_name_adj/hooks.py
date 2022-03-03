# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    lots = env["stock.production.lot"].search([("removal_date_str1", "=", False)])
    for lot in lots.with_context(tz="Japan"):
        if lot.removal_date:
            removal_date = fields.Datetime.context_timestamp(lot, lot.removal_date)
            lot.removal_date_str1 = removal_date.date().strftime("%Y%m%d")
            lot.removal_date_str2 = removal_date.date().strftime("%Y-%m-%d")
            lot.removal_date_str3 = removal_date.date().strftime("%Y/%m/%d")
