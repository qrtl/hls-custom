from odoo import SUPERUSER_ID, api
from openupgradelib import openupgrade


def _rename_fields(env):
    openupgrade.rename_fields(
        env,
        [
            (
                "res.partner",
                "res_partner",
                "warehouse_id",
                "sale_warehouse_id",
            ),
        ],
    )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _rename_fields(env)
