import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI CyberSafe Checker",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "name" not in st.session_state:
    st.session_state.name = ""

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.title("🛡️ AI CyberSafe Checker")
    st.caption("AI-assisted cyber safety awareness & risk insights")
    st.markdown("**Powered by Ebiklean Global**")

    name = st.text_input("Enter your name")

    if st.button("Login"):
        if name.strip() == "":
            st.warning("Please enter your name to continue.")
        else:
            st.session_state.name = name
            st.session_state.logged_in = True
            st.rerun()

# ---------------- MAIN APP ----------------
else:
    st.sidebar.success(f"Logged in as {st.session_state.name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🛡️ AI CyberSafe Checker")
    st.markdown("**Powered by Ebiklean Global**")

    st.subheader("Cyber Safety Check")

    weak_password = st.checkbox("I reuse the same password on many sites")
    unknown_links = st.checkbox("I click links from unknown emails or messages")
    no_2fa = st.checkbox("I do not use two-factor authentication (2FA)")
    public_wifi = st.checkbox("I often use public Wi-Fi without VPN")

    if st.button("Check Cyber Safety"):
        # Convert to numeric
        weak_n = int(weak_password)
        link_n = int(unknown_links)
        twofa_n = int(no_2fa)
        wifi_n = int(public_wifi)

        # Simple risk calculation
        risk_score = (weak_n + link_n + twofa_n + wifi_n) / 4

        st.success("Cyber safety analysis complete")
        st.write(f"### Estimated Cyber Risk Score: **{risk_score * 100:.1f}%**")

        if risk_score >= 0.75:
            st.error("High cyber risk detected. Immediate action recommended.")
        elif risk_score >= 0.4:
            st.warning("Moderate cyber risk detected. Improve your security habits.")
        else:
            st.success("Low cyber risk detected. Keep up good security practices.")

        # ---------------- DOWNLOADABLE REPORT ----------------
        report = f"""
🛡️ AI CYBERSAFE CHECKER REPORT
Powered by Ebiklean Global

Name: {st.session_state.name}

Risk Factors:
- Reused Passwords: {weak_password}
- Clicking Unknown Links: {unknown_links}
- No Two-Factor Authentication: {no_2fa}
- Unsafe Public Wi-Fi Usage: {public_wifi}

Estimated Cyber Risk Score: {risk_score * 100:.1f}%

Recommendations:
- Use strong, unique passwords
- Enable 2FA on all important accounts
- Avoid suspicious links
- Use VPN on public Wi-Fi

Disclaimer:
This tool provides cyber safety awareness only.
It is NOT a replacement for professional cybersecurity services.
"""

        st.download_button(
            label="📥 Download Cyber Safety Report",
            data=report,
            file_name="ai_cybersafe_report.txt",
            mime="text/plain"
        )

    st.divider()
    st.subheader("💰 Investor & Impact Overview")
    st.write(
        """
        - Rising demand for cyber safety awareness tools  
        - Suitable for schools, NGOs, SMEs, and individuals  
        - Scalable across web and mobile platforms  
        """
    )