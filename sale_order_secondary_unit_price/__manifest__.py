# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Order Secondary Unit Price',
    "summary": "",
    "description": """
    """,
    'version': '12.0.1.0.0',
    "category": "Sale",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'sale',
        'product_secondary_unit',
    ],
    "data": [
        'views/sale_order_views.xml',
    ],
}
