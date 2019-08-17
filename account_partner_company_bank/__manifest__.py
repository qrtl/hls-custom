# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Company Bank',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'description': """
Adds Remit-to Bank Account field in partner.
    """,
    'author': 'Quartile Limited',
    'depends': [
        'account',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
