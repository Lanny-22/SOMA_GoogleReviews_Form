import logging

import requests

logger = logging.getLogger(__name__)


def post_webhook(url: str, payload: dict) -> tuple[bool, str]:
    """Returns (success, error_message). error_message is empty on success."""
    if not url or not url.strip():
        return False, "ZAPIER_WEBHOOK is not set in Streamlit secrets."

    try:
        response = requests.post(url.strip(), json=payload, timeout=15)
        response.raise_for_status()
        return True, ""
    except requests.HTTPError as exc:
        logger.exception("Webhook HTTP error for %s", url)
        status = exc.response.status_code if exc.response is not None else "unknown"
        return False, f"Zapier returned HTTP {status}. Check that the webhook URL matches your Zap."
    except requests.RequestException as exc:
        logger.exception("Webhook request failed for %s", url)
        return False, f"Could not reach Zapier: {exc}"
