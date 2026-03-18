import json
import logging


_logger = logging.getLogger(__name__)


def post_init_hook(env):
    summary = env["stock.svl.remaining.repair.service"].sudo().run_post_init_repair()
    _logger.warning("stock_svl_remaining_repair summary: %s", json.dumps(summary, ensure_ascii=False, default=str))
