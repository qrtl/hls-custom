# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Scondary UoM ',
    'version': '12.0.1.1.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Accounting',
    'license': "AGPL-3",
    'description': """
Adds secondary UoM and the converted qty in account invoice.
This module borrows much of the logic from OCA sale_order_secondary_unit.
    """,
    'depends': [
        'account',
        'sale_order_secondary_unit',
    ],
    'data': [
        'views/account_invoice_views.xml',
    ],
    'installable': True,
}
