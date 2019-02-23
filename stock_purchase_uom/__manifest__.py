# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Purchase UoM ',
    'version': '11.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': """
Adds purchase UoM and the converted qty in stock quant.
    """,
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_quant_views.xml',
    ],
    'installable': True,
}
