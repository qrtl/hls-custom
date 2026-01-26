# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Move Delivery Slip Required",
    "summary": "Require delivery slips on customer invoices by partner",
    "version": "18.0.1.0.0",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "category": "Accounting",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
