import os
import re
from typing import Tuple

import streamlit as st

ZAPIER_URL_PATTERN = re.compile(
    r"^https://hooks\.zapier\.com/hooks/catch/.+",
    re.IGNORECASE,
)

DEFAULT_GOOGLE_REVIEW_URL = "https://g.page/r/CV36gRVQ7mz_EAE/review"
DEFAULT_DISCOUNT_CODE = "SOMA_REVIEW_5"


def _secret(key: str, default: str = "") -> str:
    try:
        if key in st.secrets:
            value = st.secrets[key]
            return str(value).strip() if value is not None else default
    except Exception:
        pass
    return os.getenv(key, default).strip()


def get_google_review_url() -> str:
    return _secret("GOOGLE_REVIEW_URL", DEFAULT_GOOGLE_REVIEW_URL)


def get_zapier_webhook() -> str:
    return _secret("ZAPIER_WEBHOOK") or _secret("ZAPIER_REGISTER_WEBHOOK")


def get_discount_code() -> str:
    return _secret("DISCOUNT_CODE", DEFAULT_DISCOUNT_CODE)


def webhook_status() -> Tuple[bool, str]:
    webhook = get_zapier_webhook()
    if not webhook:
        return False, "ZAPIER_WEBHOOK is missing from Streamlit secrets."

    if not ZAPIER_URL_PATTERN.match(webhook):
        return (
            False,
            "ZAPIER_WEBHOOK does not look like a Zapier Catch Hook URL. "
            "It should start with https://hooks.zapier.com/hooks/catch/",
        )

    return True, "Webhook URL loaded from secrets."
