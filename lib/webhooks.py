import logging

import requests

logger = logging.getLogger(__name__)


def post_webhook(url: str, payload: dict) -> bool:
    if not url:
        return False

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("Webhook request failed for %s", url)
        return False
