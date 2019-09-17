# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Line ',
    'version': '12.0.1.1.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Accounting',
    'license': "AGPL-3",
    'description': """
Adjust Account Invoice Line View
- Display Sale Order Name
- Default sort by Sale Order Name.
    """,
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'views/account_invoice_views.xml',
    ],
    'installable': True,
}
