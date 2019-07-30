# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Report',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'license': 'AGPL-3',
    'description': """
Adds an invoice report in desired layout.
    """,
    'author': 'Quartile Limited',
    'depends': [
        'account',
        'report_common_hls',
        'report_py3o',
    ],
    'data': [
        'report.xml',
        'views/res_company_views.xml',
        # 'views/res_partner_views.xml',
    ],
    'installable': True,
}
