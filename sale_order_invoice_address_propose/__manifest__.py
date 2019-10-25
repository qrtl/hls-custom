# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Order Invoice Address Propose',
    'version': '12.0.1.0.2',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Sales',
    'license': "AGPL-3",
    'description': """
Add Invoice Address to contact model, and propose Invoice Address of 
the sales order based on the selected Delivery Address.
    """,
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
