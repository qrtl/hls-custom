# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Dispatch Option",
    "version": "12.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Invoice",
    "license": "AGPL-3",
    "depends": ["sale_stock"],
    "data": [
        "views/res_partner_views.xml",
        "views/account_invoice_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
