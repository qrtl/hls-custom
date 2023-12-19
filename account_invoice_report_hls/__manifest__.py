# Copyright 2019-2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Report",
    "version": "12.0.1.2.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "depends": [
        "sale_stock",
        "report_common_hls",
        "account_partner_company_bank",
        "account_invoice_secondary_unit_price",
        "sale_order_delivery_date",
        "sale_order_line_customer_reference",
        "stock_secondary_unit",
        "uom_dp",
    ],
    "data": [
        "data/account_invoice_data.xml",
        "data/report_paperformat_data.xml",
        "report/invoice_delivery_report.xml",
        "report/report_invoice_delivery_templates.xml",
        "views/res_company_views.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
}
