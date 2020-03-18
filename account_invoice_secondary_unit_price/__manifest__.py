# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Secondary UoM Price",
    "version": "12.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Accounting",
    "license": "AGPL-3",
    "description": """
Adds Secondary Unit Price and the converted price in account invoice line.
    """,
    "depends": ["account_invoice_secondary_unit",],
    "data": ["views/account_invoice_views.xml",],
    "installable": True,
}
