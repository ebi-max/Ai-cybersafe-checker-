import streamlit as st
from datetime import datetime
import json

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="AI CyberSafe Checker",
    page_icon="🔐",
    layout="centered"
)

# ---------------------------------
# Header / Branding
# ---------------------------------
st.markdown("""
<h2 style="text-align:center;">🔐 AI CyberSafe Checker</h2>
<p style="text-align:center; font-weight:bold;">Powered by Ebiklean Global</p>
<p style="text-align:center;">AI-powered digital safety & phishing awareness</p>
<hr>
""", unsafe_allow_html=True)

# ---------------------------------
# Session State
# ---------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------------
# Login (Safe & Simple)
# ---------------------------------
if st.session_state.user is None:
    name = st.text_input("Enter your name to continue")
    if st.button("Login"):
        if name.strip():
            st.session_state.user = name
            st.rerun()
        else:
            st.warning("Please enter your name")
    st.stop()

st.success(f"Welcome, {st.session_state.user} 👋")

# ---------------------------------
# Notifications
# ---------------------------------
st.info("🔔 Tip: Never share OTPs, passwords, or private keys online.")

# ---------------------------------
# Cyber Risk Input
# ---------------------------------
st.subheader("🛡 Cyber Safety Check")

email_links = st.selectbox(
    "Do you click links from unknown emails?",
    ["Never", "Sometimes", "Often"]
)

password_reuse = st.selectbox(
    "Do you reuse passwords across platforms?",
    ["No", "Yes"]
)

two_fa = st.selectbox(
    "Do you use Two-Factor Authentication (2FA)?",
    ["Yes", "No"]
)

# ---------------------------------
# Classification Logic
# ---------------------------------
def cyber_risk_classifier(links, reuse, twofa):
    if links == "Often" or reuse == "Yes" or twofa == "No":
        return "High Risk", "⚠️ High exposure to phishing or account compromise."
    elif links == "Sometimes":
        return "Moderate Risk", "⚠️ Improve cyber hygiene habits."
    else:
        return "Low Risk", "✅ Good cyber safety practices."

# ---------------------------------
# Run Assessment
# ---------------------------------
if st.button("Run CyberSafe Check"):
    risk, advice = cyber_risk_classifier(email_links, password_reuse, two_fa)

    st.subheader("🧠 Cyber Risk Assessment")
    st.write(f"**Risk Level:** {risk}")
    st.write(f"**Advice:** {advice}")

    report = {
        "Name": st.session_state.user,
        "Clicks Unknown Links": email_links,
        "Password Reuse": password_reuse,
        "Uses 2FA": two_fa,
        "Risk Level": risk,
        "Advice": advice,
        "Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    st.download_button(
        "📥 Download Cyber Safety Report",
        json.dumps(report, indent=4),
        file_name="ai_cybersafe_report.json",
        mime="application/json"
    )

# ---------------------------------
# Awareness Gallery
# ---------------------------------
st.markdown("---")
st.subheader("🖼 Cyber Safety Awareness")

st.image(
    [
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
        "https://images.unsplash.com/photo-1510511459019-5dda7724fd87"
    ],
    caption=["Avoid Phishing Attacks", "Protect Your Digital Identity"],
    use_column_width=True
)

# ---------------------------------
# Chat Assistant
# ---------------------------------
st.markdown("---")
st.subheader("💬 Cyber Assistant Chat")

user_msg = st.text_input("Ask a cyber safety question")

if st.button("Send"):
    if user_msg:
        st.session_state.chat.append(("You", user_msg))
        st.session_state.chat.append(
            ("AI", "I provide general cyber safety guidance. Stay alert online.")
        )

for sender, msg in st.session_state.chat:
    st.write(f"**{sender}:** {msg}")

# ---------------------------------
# Impact / Investor Dashboard
# ---------------------------------
st.markdown("---")
st.subheader("📊 Impact & Investor Snapshot")

c1, c2, c3 = st.columns(3)

c1.metric("Primary Threat", "Phishing")
c2.metric("Target Users", "Internet Users")
c3.metric("Scalability", "Very High")

st.info(
    "AI CyberSafe Checker improves digital safety awareness and reduces phishing "
    "and social engineering risks at scale."
)

# ---------------------------------
# Link to Other Apps
# ---------------------------------
st.markdown("---")
st.subheader("🌍 Explore Other Tools")

st.markdown(
    "➡️ **AI Health Checker** – Health awareness & early risk insights"
)

# ---------------------------------
# Footer
# ---------------------------------
st.markdown("""
<hr>
<p style="text-align:center; font-size:12px;">
© 2026 Ebiklean Global • AI for Social Good
</p>
""", unsafe_allow_html=True)