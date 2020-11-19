# Copyright 2019-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Report",
    "version": "12.0.1.2.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "depends": [
        "sale_stock",
        "report_common_hls",
        "report_py3o",
        "account_partner_company_bank",
        "account_invoice_secondary_unit_price",
        "stock_picking_delivery_due_date",
        "sale_order_line_customer_reference",
    ],
    "data": [
        "views/res_company_views.xml",
        "views/account_invoice_views.xml",
        "wizard/invoice_delivery_report_wizard_views.xml",
        "report/invoice_delivery_report.xml",
    ],
    "installable": True,
}
