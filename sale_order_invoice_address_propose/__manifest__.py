# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Order Invoice Address Propose',
    'version': '12.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Sales',
    'license': "AGPL-3",
    'description': """
Add "Invoice Address" to contact model, propose the set "Invoice Address" of 
the sale order if the "Delivery Address" is selected 
    """,
    'depends': [
        'sale',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
