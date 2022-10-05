# Copyright 2020-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.osv import expression


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    removal_date_str1 = fields.Char(
        compute="_compute_removal_date_string",
        store=True,
        copy=False,
    )
    removal_date_str2 = fields.Char(
        compute="_compute_removal_date_string",
        store=True,
        copy=False,
    )
    removal_date_str3 = fields.Char(
        compute="_compute_removal_date_string",
        store=True,
        copy=False,
    )

    @api.depends("removal_date")
    def _compute_removal_date_string(self):
        # Apply company's timezone if available.
        tz = self.env.user.company_id.partner_id.tz or "Japan"
        for lot in self.with_context(tz=tz):
            if lot.removal_date:
                removal_date = fields.Datetime.context_timestamp(self, lot.removal_date)
                lot.removal_date_str1 = removal_date.date().strftime("%Y/%m/%d")
                lot.removal_date_str2 = removal_date.date().strftime("%Y-%m-%d")
                lot.removal_date_str3 = removal_date.date().strftime("%Y%m%d")

    @api.multi
    def name_get(self):
        result = []
        for lot in self:
            name = lot.name
            if lot.removal_date_str1:
                name = "[" + lot.removal_date_str1 + "] " + lot.name
            result.append((lot.id, name))
        return result

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            # Tried below first and it turned out that the search with the date (e.g.
            # '2023-09-01') on removal_date somehow wouldn't work.
            # domain = ['|', ('removal_date', '=like', '%' + name.replace('/', '-') + '%'), ('name', operator, name)]  # noqa
            removal_date = "%" + name + "%"
            domain = [
                "|",
                "|",
                "|",
                ("removal_date_str1", operator, removal_date),
                ("removal_date_str2", operator, removal_date),
                ("removal_date_str3", operator, removal_date),
                ("name", operator, name),
            ]
        lot_ids = self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )
        return self.browse(lot_ids).name_get()
