import uuid
from datetime import datetime, timezone
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

from lib.config import (
    APP_BASE_URL,
    CLAIM_MIN_DELAY_SECONDS,
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
    "Share your honest experience on Google, then claim your thank-you offer "
    "for your next class."
)

if "step" not in st.session_state:
    st.session_state.step = "form"
if "claim_token" not in st.session_state:
    st.session_state.claim_token = ""
if "claim_url" not in st.session_state:
    st.session_state.claim_url = ""


def claim_url_for(token: str) -> str:
    return f"{APP_BASE_URL}/claim?token={quote(token)}"


def handle_registration(first_name: str, last_name: str, email: str) -> None:
    normalized_email = email.strip().lower()

    if email_exists(normalized_email):
        st.error(
            "This email has already been registered. "
            "Use your original claim link or contact the studio if you need help."
        )
        return

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

    st.session_state.step = "success"
    st.session_state.claim_token = token
    st.session_state.claim_url = claim_url


if st.session_state.step == "form":
    st.markdown(
        '<span class="soma-step-label">Step 1 of 2</span>',
        unsafe_allow_html=True,
    )

    with st.form("review_registration_form", clear_on_submit=False):
        first_name = st.text_input("First name", autocomplete="given-name")
        last_name = st.text_input("Last name", autocomplete="family-name")
        email = st.text_input(
            "Email",
            help="Use the same email you use for Momence bookings.",
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

if st.session_state.step == "success":
    st.markdown(
        '<div class="soma-success-box">'
        "You're registered. Google Reviews should open in a new tab."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="soma-info-box">
          <strong>Step 2:</strong> After posting your review on Google, return here and
          claim your thank-you offer. We will email your discount code to the address
          you provided.
          <br /><br />
          <a href="{st.session_state.claim_url}">{st.session_state.claim_url}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "Leave a Google Review",
        GOOGLE_REVIEW_URL,
        type="primary",
        use_container_width=True,
    )

    st.link_button(
        "Claim my thank-you offer",
        st.session_state.claim_url,
        use_container_width=True,
    )

    components.html(
        f"""
        <script>
          window.open("{GOOGLE_REVIEW_URL}", "_blank");
        </script>
        """,
        height=0,
    )

    delay_minutes = max(1, CLAIM_MIN_DELAY_SECONDS // 60)
    st.caption(
        f"The claim link becomes active about {delay_minutes} minutes after you register, "
        "giving you time to post your review."
    )
