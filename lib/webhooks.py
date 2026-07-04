from typing import Tuple

import requests


def post_webhook(url: str, payload: dict) -> Tuple[bool, str]:
    clean_url = (url or "").strip()
    if not clean_url:
        return False, "ZAPIER_WEBHOOK is not set in Streamlit secrets."

    headers = {
        "User-Agent": "SOMA-GoogleReviews-Form/1.0",
        "Accept": "application/json",
    }

    try:
        response = requests.post(
            clean_url,
            json=payload,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
        return True, ""
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        body = (exc.response.text or "").strip()[:200] if exc.response is not None else ""
        detail = f" Response: {body}" if body else ""
        return (
            False,
            f"Zapier returned HTTP {status}.{detail} "
            "Copy the Catch Hook URL again from the Zap trigger step.",
        )
    except requests.RequestException as exc:
        return False, f"Could not reach Zapier: {exc}"
