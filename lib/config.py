import os
import re

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

ZAPIER_URL_PATTERN = re.compile(
    r"^https://hooks\.zapier\.com/hooks/catch/.+",
    re.IGNORECASE,
)


def _secret(key: str, default: str = "") -> str:
    try:
        if key in st.secrets:
            value = st.secrets[key]
            return str(value).strip() if value is not None else default
    except StreamlitSecretNotFoundError:
        pass
    except Exception:
        pass
    return os.getenv(key, default).strip()


GOOGLE_REVIEW_URL = _secret(
    "GOOGLE_REVIEW_URL",
    "https://g.page/r/CV36gRVQ7mz_EAE/review",
)
ZAPIER_WEBHOOK = _secret("ZAPIER_WEBHOOK") or _secret("ZAPIER_REGISTER_WEBHOOK")
DISCOUNT_CODE = _secret("DISCOUNT_CODE", "SOMA_REVIEW_5")


def webhook_status() -> tuple[bool, str]:
    if not ZAPIER_WEBHOOK:
        return False, "ZAPIER_WEBHOOK is missing from Streamlit secrets."

    if not ZAPIER_URL_PATTERN.match(ZAPIER_WEBHOOK):
        return (
            False,
            "ZAPIER_WEBHOOK does not look like a Zapier Catch Hook URL. "
            "It should start with https://hooks.zapier.com/hooks/catch/",
        )

    return True, "Webhook URL loaded from secrets."
