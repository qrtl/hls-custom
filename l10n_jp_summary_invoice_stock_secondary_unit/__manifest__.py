# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Summary Invoice Stock Secondary Unit",
    "summary": "Display stock secondary unit quantities in summary invoices",
    "version": "18.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "depends": [
        "l10n_jp_summary_invoice_secondary_unit",
        "stock_secondary_unit",
    ],
    "data": [
        "report/report_summary_invoice_templates.xml",
    ],
    "installable": True,
}
