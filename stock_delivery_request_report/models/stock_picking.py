# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    report_address = fields.Char(
        compute="_compute_report_address",
    )
    # adding field show the date in user's timezone
    delivery_due_report_date = fields.Date(
        compute="_compute_report_delivery_due_date",
    )
    scheduled_date = fields.Datetime(string="Scheduled DateTime")
    scheduled_date_custom = fields.Date(
        string="Scheduled Date",
        compute="_compute_scheduled_date_custom",
        store=True,
    )

    @api.multi
    @api.depends("scheduled_date")
    def _compute_scheduled_date_custom(self):
        for picking in self:
            if picking.scheduled_date:
                picking.scheduled_date_custom = fields.Date.to_date(
                    fields.Datetime.context_timestamp(self, picking.scheduled_date)
                )

    @api.multi
    def _compute_report_address(self):
        for picking in self:
            partner = picking.partner_id
            address = ""
            address += partner.state_id.name if partner.state_id else ""
            address += partner.city if partner.city else ""
            address += partner.street if partner.street else ""
            address += "\n" + partner.street2 if partner.street2 else ""
            picking.report_address = address

    @api.multi
    def _compute_report_delivery_due_date(self):
        for picking in self:
            if picking.delivery_due_date:
                picking.delivery_due_report_date = fields.Date.to_date(
                    fields.Datetime.context_timestamp(self, picking.delivery_due_date)
                )

    @api.multi
    def delivery_request_form(self):
        return {
            "name": _("Delivery Request Form"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": "stock.picking.report.wizard",
            "view_id": self.env.ref(
                "stock_delivery_request_report.stock_picking_report_wizard"
            ).id,
            "type": "ir.actions.act_window",
            "context": {"picking_ids": self.env.context.get("active_ids")},
            "target": "new",
        }
