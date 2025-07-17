import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ---------------- CONFIG ----------------

SHEET_URL = "https://docs.google.com/spreadsheets/d/1ig9XBMyz1IXwxO8qznlQJ6Wv4u21x7hkVXN0abZbBjo/edit#gid=0"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-phishing"
headers = {}

# ---------------- FUNCTIONS ----------------

@st.cache_data
def load_users():
    df = pd.read_csv(SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid="))
    users = {
        row['username']: {
            'name': row['name'],
            'password': row['password'],
            'access_level': row.get('access_level', 'free'),
            'scan_count': row.get('scan_count', 0),
            'last_scan_date': row.get('last_scan_date', '')
        }
        for _, row in df.iterrows()
    }
    return users

def get_user_info(username):
    df = pd.read_csv(SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid="))
    row = df[df['username'] == username].iloc[0]
    return row.to_dict()

# ---------------- UI ----------------

st.set_page_config(page_title="AI CyberSafe Checker", layout="centered")
st.title("🛡️ AI CyberSafe Checker")

menu = st.sidebar.radio("Choose Action", ["Login", "Sign Up"])

if menu == "Sign Up":
    st.subheader("🔐 Create a New Account")
    new_name = st.text_input("Your Full Name")
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")

    if st.button("Create Account"):
        if new_user and new_pass and new_name:
            hashed_pass = stauth.Hasher([new_pass]).generate()[0]
            new_row = pd.DataFrame([[new_user, hashed_pass, new_name, 'free', 0, datetime.now().date()]], columns=["username", "password", "name", "access_level", "scan_count", "last_scan_date"])
            df = pd.read_csv(SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid="))
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("users_temp.csv", index=False)
            st.success("Account created! Now you can log in.")
        else:
            st.warning("Please fill all fields.")

else:
    st.subheader("🔓 Login to Continue")

    users = load_users()
    authenticator = stauth.Authenticate(users, "cybersafe", "auth", cookie_expiry_days=1)
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status == False:
        st.error("Invalid credentials.")
    elif auth_status == None:
        st.warning("Enter your login info.")
    elif auth_status:
elif auth_status:
    authenticator.logout("Logout", "sidebar")

    st.success(f"🎉 Welcome, {name} 👋 You're now logged in to AI CyberSafe Checker.")
    if users[username]["access"] == "premium":
        st.info("✅ Premium access: You can run unlimited scam message checks every day.")
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        scan_count = int(users[username]["scan_count"]) if users[username]["last_scan_date"] == today else 0
        remaining = 3 - scan_count
        st.info(f"💡 Free access: You can scan {remaining} more messages today. Upgrade for unlimited access!")

    st.markdown("### Paste the suspicious message below:")

        # Free users: Max 5 scans per day
        can_scan = True
        if access_level != "premium":
            if last_date == scan_date:
                if scan_count >= 5:
                    can_scan = False
            else:
                scan_count = 0

        if message:
            if can_scan or access_level == "premium":
                with st.spinner("Analyzing with AI..."):
                    response = requests.post(API_URL, headers=headers, json={"inputs": message})
                    result = response.json()[0]
                    label = result['label']
                    score = round(result['score'] * 100, 2)

                    if label.lower() == "phishing":
                        st.error(f"🚨 SCAM DETECTED ({score}%)")
                    else:
                        st.success(f"✅ SAFE ({score}%)")

                # update scan count
                df = pd.read_csv(SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid="))
                df.loc[df['username'] == username, 'scan_count'] = scan_count + 1
                df.loc[df['username'] == username, 'last_scan_date'] = scan_date
                df.to_csv("users_temp.csv", index=False)
            else:
                st.warning("Daily scan limit reached. Upgrade to unlock full access.")

        # Payment Instructions for Upgrade
        if access_level != "premium":
            st.markdown("""
                ---
                ### 🔓 Want Unlimited Access?
                Free users are limited to 5 scam scans daily.

                To unlock unlimited usage:

                📌 **Pay ₦500** to:

                - **Name:** Ebieme Bassey  
                - **Bank:** Fidelity Bank  
                - **Account Number:** 6681569396

                After payment, send proof via WhatsApp:
                👉 [Click to chat](https://wa.me/2347031204549

                You'll be upgraded manually within 5 minutes after confirmation.
            """)