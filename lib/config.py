import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


def _secret(key: str, default: str = "") -> str:
    try:
        if key in st.secrets:
            value = st.secrets[key]
            return str(value) if value is not None else default
    except StreamlitSecretNotFoundError:
        pass
    except Exception:
        pass
    return os.getenv(key, default)


GOOGLE_REVIEW_URL = _secret(
    "GOOGLE_REVIEW_URL",
    "https://g.page/r/CV36gRVQ7mz_EAE/review",
)
ZAPIER_WEBHOOK = _secret("ZAPIER_WEBHOOK") or _secret("ZAPIER_REGISTER_WEBHOOK")
DISCOUNT_CODE = _secret("DISCOUNT_CODE", "SOMA_REVIEW_5")
