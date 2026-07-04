from datetime import datetime, timezone

import streamlit as st

from lib.config import (
    APP_BASE_URL,
    CLAIM_MIN_DELAY_SECONDS,
    DISCOUNT_CODE,
    ZAPIER_CLAIM_WEBHOOK,
)
from lib.storage import get_submission, init_db, mark_claimed
from lib.styles import inject_global_styles
from lib.webhooks import post_webhook

st.set_page_config(
    page_title="Claim your offer — SOMA Pilates",
    page_icon="🎁",
    layout="centered",
)

init_db()
inject_global_styles()

token = st.query_params.get("token", "").strip()

st.title("Claim your thank-you offer")
st.caption("Step 2 of 2 — we'll email your discount code after you confirm.")

if not token:
    st.warning("This claim link is missing a token. Scan the studio QR code to start again.")
    st.link_button("Back to registration", APP_BASE_URL)
    st.stop()

submission = get_submission(token)

if submission is None:
    st.error("This claim link is invalid or has expired. Please register again at the studio.")
    st.link_button("Start again", APP_BASE_URL)
    st.stop()

if submission["claimed_at"]:
    st.info(
        f"A discount code was already sent to **{submission['email']}**. "
        "Check your inbox and spam folder."
    )
    st.stop()

created_at = datetime.fromisoformat(submission["created_at"])
now = datetime.now(timezone.utc)
elapsed_seconds = (now - created_at).total_seconds()
remaining_seconds = CLAIM_MIN_DELAY_SECONDS - elapsed_seconds

if remaining_seconds > 0:
    remaining_minutes = int(remaining_seconds // 60) + 1
    st.warning(
        f"Please finish posting your Google review first. "
        f"You can claim your offer in about {remaining_minutes} minute(s)."
    )
    st.caption(
        "This short wait gives you time to share your experience on Google before "
        "we send your code."
    )
    st.stop()

st.markdown(
    f"""
    <div class="soma-info-box">
      Hi <strong>{submission["first_name"]}</strong>, confirm below and we'll email your
      discount code to <strong>{submission["email"]}</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Email my discount code", type="primary", use_container_width=True):
    sent = post_webhook(
        ZAPIER_CLAIM_WEBHOOK,
        {
            "event": "review_offer_claimed",
            "first_name": submission["first_name"],
            "last_name": submission["last_name"],
            "email": submission["email"],
            "claim_token": token,
            "discount_code": DISCOUNT_CODE,
            "claimed_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    if not ZAPIER_CLAIM_WEBHOOK:
        st.error(
            "The claim webhook is not configured yet. "
            "Add ZAPIER_CLAIM_WEBHOOK to your environment or Streamlit secrets."
        )
    elif not sent:
        st.error(
            "We couldn't send your code right now. Please try again in a moment "
            "or contact the studio."
        )
    else:
        mark_claimed(token)
        st.success(
            f"Done! Check **{submission['email']}** for your discount code. "
            "If you don't see it within a few minutes, check spam."
        )
