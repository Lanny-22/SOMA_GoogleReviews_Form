import json

import streamlit as st
import streamlit.components.v1 as components


def redirect_to_external_url(url: str, message: str = "Redirecting to Google Reviews…") -> None:
    """Best-effort redirect for Streamlit Community Cloud (sandboxed iframes)."""
    safe_url = json.dumps(url)

    st.markdown(
        f"""
        <div class="soma-info-box">
          {message}
          <br /><br />
          <a href="{url}" target="_blank" rel="noopener noreferrer">
            Click here if you are not redirected automatically
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    components.html(
        f"""
        <!DOCTYPE html>
        <html>
          <body>
            <script>
              (function () {{
                const url = {safe_url};

                function openInNewTab() {{
                  window.open(url, "_blank", "noopener,noreferrer");
                }}

                function redirectTopWindow() {{
                  try {{
                    const link = document.createElement("a");
                    link.href = url;
                    link.target = "_top";
                    link.rel = "noopener noreferrer";
                    link.style.display = "none";
                    window.top.document.body.appendChild(link);
                    link.click();
                    link.remove();
                    return true;
                  }} catch (error) {{
                    return false;
                  }}
                }}

                function redirectSameFrame() {{
                  try {{
                    window.top.location.href = url;
                    return true;
                  }} catch (error) {{
                    return false;
                  }}
                }}

                if (!redirectTopWindow() && !redirectSameFrame()) {{
                  openInNewTab();
                }}

                setTimeout(function () {{
                  if (!redirectTopWindow() && !redirectSameFrame()) {{
                    openInNewTab();
                  }}
                }}, 300);
              }})();
            </script>
          </body>
        </html>
        """,
        height=0,
    )

    st.link_button(
        "Open Google Reviews",
        url,
        type="primary",
        use_container_width=True,
    )
    st.stop()
