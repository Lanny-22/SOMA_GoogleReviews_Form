import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
          .stApp,
          [data-testid="stAppViewContainer"],
          [data-testid="stMain"],
          [data-testid="stHeader"],
          [data-testid="stBottom"],
          [data-testid="stMainBlockContainer"],
          [data-testid="block-container"] {
            background-color: #fcf1eb !important;
          }

          [data-testid="stMainBlockContainer"] {
            max-width: 560px;
            padding-top: 2rem;
          }

          h1, h2, h3, p, label, .stMarkdown {
            color: #03010d;
          }

          div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid rgba(16, 89, 95, 0.12);
            border-radius: 16px;
            padding: 1.5rem 1.25rem 1.25rem;
            box-shadow: 0 8px 24px rgba(3, 1, 13, 0.06);
          }

          div[data-testid="stForm"] label {
            font-weight: 600;
            font-size: 0.92rem;
          }

          div[data-testid="stForm"] input {
            border-radius: 10px;
            border: 1px solid rgba(16, 89, 95, 0.18);
            min-height: 44px;
          }

          div[data-testid="stFormSubmitButton"] > button {
            width: 100%;
            border-radius: 999px;
            min-height: 48px;
            font-weight: 700;
            background: rgb(16, 89, 95) !important;
            color: #ffffff !important;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
          }

          div[data-testid="stFormSubmitButton"] > button:hover,
          div[data-testid="stFormSubmitButton"] > button:focus,
          div[data-testid="stFormSubmitButton"] > button:active {
            background: rgb(12, 68, 73) !important;
            color: #ffffff !important;
            border: none;
          }

          div[data-testid="stFormSubmitButton"] > button p,
          div[data-testid="stFormSubmitButton"] > button span,
          div[data-testid="stFormSubmitButton"] > button div {
            color: #ffffff !important;
            text-align: center;
            width: 100%;
            margin: 0;
          }

          .soma-success-box {
            background: #edf9f2;
            border: 1px solid #b7e4c7;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            color: #0d8050;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 1rem;
          }

          .soma-info-box {
            background: #ffffff;
            border: 1px solid rgba(16, 89, 95, 0.12);
            border-radius: 12px;
            padding: 1rem 1.1rem;
            line-height: 1.55;
            margin-bottom: 1rem;
          }

          .soma-step-label {
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: rgb(16, 89, 95);
            margin-bottom: 0.35rem;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
  <style>
    :root {
      --momenceColorBackground: #fcf1eb;
      --momenceColorPrimary: 16, 89, 95;
      --momenceColorBlack: 3, 1, 13;
    }
    html, body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 0;
      background: #fcf1eb;
      color: rgb(var(--momenceColorBlack));
    }
    .momence-form-shell {
      background: #ffffff;
      border: 1px solid rgba(var(--momenceColorPrimary), 0.12);
      border-radius: 16px;
      padding: 20px 18px 18px;
      box-shadow: 0 8px 24px rgba(3, 1, 13, 0.06);
    }
    .momence-form-shell h2 {
      margin: 0 0 6px;
      font-size: 1.15rem;
    }
    .momence-form-shell p {
      margin: 0 0 16px;
      color: rgba(3, 1, 13, 0.72);
      line-height: 1.5;
      font-size: 0.95rem;
    }
    .field {
      margin-bottom: 14px;
    }
    label {
      display: block;
      font-size: 0.92rem;
      font-weight: 600;
      margin-bottom: 6px;
    }
    input {
      width: 100%;
      box-sizing: border-box;
      min-height: 44px;
      border-radius: 10px;
      border: 1px solid rgba(var(--momenceColorPrimary), 0.18);
      padding: 10px 12px;
      font-size: 1rem;
    }
    input:focus {
      outline: 2px solid rgba(var(--momenceColorPrimary), 0.25);
      border-color: rgb(var(--momenceColorPrimary));
    }
    button {
      width: 100%;
      min-height: 48px;
      border: none;
      border-radius: 999px;
      background: rgb(var(--momenceColorPrimary));
      color: #fff;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      margin-top: 4px;
    }
    button:hover {
      background: rgb(12, 68, 73);
    }
    .form-error {
      display: none;
      margin: 0 0 12px;
      padding: 10px 12px;
      border-radius: 8px;
      background: #fde8e8;
      color: #9b1c1c;
      font-size: 14px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="momence-form-shell">
    <h2>Share your experience</h2>
    <p>Tell us who you are, then leave us an honest Google review. After that, come back to claim your thank-you offer.</p>
    <p id="form-error" class="form-error"></p>
    <form id="review-form">
      <div class="field">
        <label for="firstName">First name</label>
        <input id="firstName" name="firstName" type="text" required autocomplete="given-name" />
      </div>
      <div class="field">
        <label for="lastName">Last name</label>
        <input id="lastName" name="lastName" type="text" required autocomplete="family-name" />
      </div>
      <div class="field">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required autocomplete="email" />
      </div>
      <button type="submit">Continue to Google Review</button>
    </form>
  </div>
  <script>
    const form = document.getElementById("review-form");
    const errorEl = document.getElementById("form-error");

    function showError(message) {
      errorEl.textContent = message;
      errorEl.style.display = "block";
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      errorEl.style.display = "none";

      const firstName = document.getElementById("firstName").value.trim();
      const lastName = document.getElementById("lastName").value.trim();
      const email = document.getElementById("email").value.trim();

      if (!firstName || !lastName || !email) {
        showError("Please complete all fields.");
        return;
      }

      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        showError("Please enter a valid email address.");
        return;
      }

      window.parent.postMessage(
        {
          isStreamlitMessage: true,
          type: "streamlit:setComponentValue",
          value: {
            firstName,
            lastName,
            email,
          },
        },
        "*"
      );
    });
  </script>
</body>
</html>
"""
