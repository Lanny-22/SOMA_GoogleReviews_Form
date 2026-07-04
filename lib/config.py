import os

import streamlit as st


def _secret(key: str, default: str = "") -> str:
    if key in st.secrets:
        return str(st.secrets[key])
    return os.getenv(key, default)


GOOGLE_REVIEW_URL = _secret(
    "GOOGLE_REVIEW_URL",
    "https://g.page/r/CV36gRVQ7mz_EAE/review",
)
ZAPIER_WEBHOOK = _secret("ZAPIER_WEBHOOK") or _secret("ZAPIER_REGISTER_WEBHOOK")
DISCOUNT_CODE = _secret("DISCOUNT_CODE", "SOMA_REVIEW_5")
