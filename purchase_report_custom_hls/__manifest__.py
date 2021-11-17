# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Purchase Order Report Custom",
    "version": "12.0.1.0.0",
    "category": "Purchase",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["purchase_stock", "report_common_hls"],
    "data": [
        "security/purchase_security.xml",
        "report/purchase_order_report_templates.xml",
        "views/purchase_order_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
