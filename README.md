import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ---------------- CONFIG ----------------
# Google Sheets Setup
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ig9XBMyz1IXwxO8qznlQJ6Wv4u21x7hkVXN0abZbBjo/edit#gid=0"

# Google Service Account JSON setup (you must upload this to secrets later for full access)
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
# PLACEHOLDER for future use

# HuggingFace API for scam detection
API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-phishing"
headers = {}

# ---------------- FUNCTIONS ----------------

@st.cache_data
def load_users():
    df = pd.read_csv(SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid="))
    users = {
        row['username']: {
            'name': row['name'],
            'password': row['password']
        } for _, row in df.iterrows()
    }
    return users

def add_user_to_sheet(username, name, password_hashed):
    # Build the correct link for appending data
    csv_url = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(csv_url)
    new_row = pd.DataFrame([[username, password_hashed, name]], columns=["username", "password", "name"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("users_temp.csv", index=False)
    st.success("Account created! Now you can log in.")

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
            add_user_to_sheet(new_user, new_name, hashed_pass)
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
        authenticator.logout("Logout", "sidebar")
        st.sidebar.success(f"Welcome {name} 👋")

        # -------- APP MAIN FUNCTION --------
        st.write("Paste any suspicious message below to detect scams.")
        message = st.text_area("✉️ Message to Analyze:")

        if message:
            with st.spinner("Analyzing..."):
                response = requests.post(API_URL, headers=headers, json={"inputs": message})
                result = response.json()[0]
                label = result['label']
                score = round(result['score'] * 100, 2)

                if label.lower() == "phishing":
                    st.error(f"🚨 SCAM DETECTED ({score}%)")
                else:
                    st.success(f"✅ SAFE ({score}%)")
