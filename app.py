import uuid
from datetime import datetime, timezone
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

from lib.config import (
    APP_BASE_URL,
    DISCOUNT_CODE,
    GOOGLE_REVIEW_URL,
    ZAPIER_REGISTER_WEBHOOK,
)
from lib.storage import create_submission, email_exists, init_db
from lib.styles import inject_global_styles
from lib.webhooks import post_webhook

st.set_page_config(
    page_title="SOMA Pilates — Google Review",
    page_icon="✨",
    layout="centered",
)

init_db()
inject_global_styles()

st.title("Thank you for visiting SOMA")
st.caption(
    "Enter your details below — you'll be taken straight to Google to leave your review. "
    "We'll email you a link to claim your thank-you offer afterwards."
)


def claim_url_for(token: str) -> str:
    return f"{APP_BASE_URL}/claim?token={quote(token)}"


def redirect_to_google_review() -> None:
    st.markdown(
        f'<meta http-equiv="refresh" content="0;url={GOOGLE_REVIEW_URL}">',
        unsafe_allow_html=True,
    )
    components.html(
        f"""
        <script>
          window.top.location.replace("{GOOGLE_REVIEW_URL}");
        </script>
        """,
        height=0,
    )
    st.stop()


def handle_registration(first_name: str, last_name: str, email: str) -> bool:
    normalized_email = email.strip().lower()

    if email_exists(normalized_email):
        st.error(
            "This email has already been registered. "
            "Check your inbox for your original claim link, or contact the studio if you need help."
        )
        return False

    token = str(uuid.uuid4())
    create_submission(token, first_name, last_name, normalized_email)

    claim_url = claim_url_for(token)
    post_webhook(
        ZAPIER_REGISTER_WEBHOOK,
        {
            "event": "review_form_submitted",
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": normalized_email,
            "claim_token": token,
            "claim_url": claim_url,
            "discount_code": DISCOUNT_CODE,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    redirect_to_google_review()
    return True


st.markdown(
    '<span class="soma-step-label">Step 1 of 2</span>',
    unsafe_allow_html=True,
)

with st.form("review_registration_form", clear_on_submit=False):
    first_name = st.text_input("First name", autocomplete="given-name")
    last_name = st.text_input("Last name", autocomplete="family-name")
    email = st.text_input(
        "Email",
        help="Use the same email you use for Momence bookings. Your claim link will be sent here.",
        autocomplete="email",
    )
    submitted = st.form_submit_button("Continue to Google Review")

if submitted:
    if not first_name.strip() or not last_name.strip() or not email.strip():
        st.error("Please complete all fields.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        st.error("Please enter a valid email address.")
    else:
        handle_registration(first_name, last_name, email)
