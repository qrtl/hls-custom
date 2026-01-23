from odoo import SUPERUSER_ID, api
from openupgradelib import openupgrade


def _rename_fields(env):
    openupgrade.rename_fields(
        env,
        [
            (
                "sale.order.line",
                "sale_order_line",
                "delivery_note",
                "note",
            ),
        ],
    )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _rename_fields(env)
