import logging
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)


@dataclass
class WebhookResult:
    ok: bool
    error: str = ""


def post_webhook(url: str, payload: dict) -> WebhookResult:
    if not url or not url.strip():
        return WebhookResult(
            ok=False,
            error="ZAPIER_WEBHOOK is not set in Streamlit secrets.",
        )

    try:
        response = requests.post(url.strip(), json=payload, timeout=15)
        response.raise_for_status()
        return WebhookResult(ok=True)
    except requests.HTTPError as exc:
        logger.exception("Webhook HTTP error for %s", url)
        status = exc.response.status_code if exc.response is not None else "unknown"
        return WebhookResult(
            ok=False,
            error=f"Zapier returned HTTP {status}. Check that the webhook URL matches your Zap.",
        )
    except requests.RequestException as exc:
        logger.exception("Webhook request failed for %s", url)
        return WebhookResult(
            ok=False,
            error=f"Could not reach Zapier: {exc}",
        )
