# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    monthly_invoice = fields.Boolean(
        "Monthly Invoice",
        default=True,
        help="If selected, shows the delivery details in the printed " "invoice.",
    )
    doc_title = fields.Char(
        "Doc Title", help="The value gets newly proposed when Invoice Date is changed."
    )
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")

    @api.onchange("date_invoice")
    def _onchange_date_invoice(self):
        for inv in self:
            date = inv.date_invoice or fields.Date.from_string(
                fields.Date.context_today(self)
            )
            inv.date_from = date.replace(day=1)
            inv.date_to = inv.date_from + relativedelta(months=1, days=-1)

    @api.onchange("date_from")
    def _onchange_date_from(self):
        for inv in self:
            inv.doc_title = str(inv.date_from.month) + "月分" if inv.date_from else False

    @api.multi
    def action_date_assign(self):
        # populate date range at validation in case the fields are not updated
        # before validating the invoice
        res = super(AccountInvoice, self).action_date_assign()
        for inv in self.filtered(
            lambda x: x.monthly_invoice and (not x.date_from or not x.date_to)
        ):
            inv._onchange_date_invoice()
            # respect the already existing doc title.
            if not inv.doc_title:
                inv._onchange_date_from()
        return res

    @api.constrains("date_from", "date_to")
    def _check_date_range(self):
        for inv in self:
            if inv.date_from and inv.date_to and inv.date_from > inv.date_to:
                raise ValidationError(_("Date To must not be earlier than Date From."))

    @api.multi
    def action_print_invoice_delivery_qweb_report(self):
        report_ref = "account_invoice_report_hls.invoice_delivery_qweb_report"
        reports = self.env["invoice.delivery.report"]._create_invoice_delivery_report(
            self
        )
        return self.env.ref(report_ref).report_action([reports.ids])
