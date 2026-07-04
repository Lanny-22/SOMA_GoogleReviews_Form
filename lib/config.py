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
APP_BASE_URL = _secret("APP_BASE_URL", "http://localhost:8501").rstrip("/")
ZAPIER_REGISTER_WEBHOOK = _secret("ZAPIER_REGISTER_WEBHOOK")
ZAPIER_CLAIM_WEBHOOK = _secret("ZAPIER_CLAIM_WEBHOOK")
CLAIM_MIN_DELAY_SECONDS = int(_secret("CLAIM_MIN_DELAY_SECONDS", "300"))
DISCOUNT_CODE = _secret("DISCOUNT_CODE", "SOMA_REVIEW_5")
