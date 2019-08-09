# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Delivery Request Form Report Py3o',
    'version': '12.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': """
This module adds one py3o stock picking report.
    """,
    'depends': [
        'stock',
        'report_py3o',
    ],
    'data': [
        'report.xml',
        'data/stock_picking_data.xml',
        'wizards/stock_picking_report_wizard_views.xml',
    ],
    'installable': True,
}
