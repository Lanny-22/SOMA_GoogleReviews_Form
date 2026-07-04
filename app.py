from datetime import datetime, timezone

import streamlit as st

from lib.config import get_discount_code, get_google_review_url, get_zapier_webhook, webhook_status
from lib.redirect import redirect_to_external_url
from lib.styles import inject_global_styles
from lib.webhooks import post_webhook

st.set_page_config(
    page_title="SOMA Pilates — Google Review",
    page_icon="✨",
    layout="centered",
)

inject_global_styles()

if "pending_google_redirect" not in st.session_state:
    st.session_state.pending_google_redirect = False

if st.session_state.pending_google_redirect:
    st.session_state.pending_google_redirect = False
    redirect_to_external_url(
        get_google_review_url(),
        "Taking you to Google Reviews now. A new tab may open if your browser requires it.",
    )

st.title("Thank you for visiting SOMA")
st.caption(
    "Enter your details below — you'll be taken to Google to leave your review, "
    "and we'll email your thank-you discount code to the address you provide."
)


def handle_registration(first_name: str, last_name: str, email: str) -> None:
    normalized_email = email.strip().lower()

    ok, status_message = webhook_status()
    if not ok:
        st.error(f"{status_message} Update Secrets and reboot the app.")
        return

    success, error = post_webhook(
        get_zapier_webhook(),
        {
            "event": "review_form_submitted",
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": normalized_email,
            "discount_code": get_discount_code(),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    if not success:
        st.error(
            f"Could not notify Zapier, so no email will be sent. {error} "
            "Fix this in Streamlit Cloud → Manage app → Settings → Secrets, then reboot."
        )
        return

    st.session_state.pending_google_redirect = True
    st.rerun()


with st.form("review_registration_form", clear_on_submit=False):
    first_name = st.text_input("First name", autocomplete="given-name")
    last_name = st.text_input("Last name", autocomplete="family-name")
    email = st.text_input(
        "Email",
        help="Use the same email you use for Momence bookings. Your discount code will be sent here.",
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
