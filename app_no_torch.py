import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime

# ---------------- CONFIG ----------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ig9XBMyz1IXwxO8qznlQJ6Wv4u21x7hkVXN0abZbBjo/edit#gid=0"
API_URL   = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-phishing"
headers   = {}          # add your HF token here later if rate-limited
FREE_LIMIT = 5          # free scans per user per day

# ---------- GOOGLE-SHEET HELPERS ----------
@st.cache_data
def get_sheet_df() -> pd.DataFrame:
    csv_url = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

def save_df(df: pd.DataFrame):
    df.to_csv("users_temp.csv", index=False)                 # tmp file Streamlit can write
    # In Community Cloud this automatically overwrites the Sheet after a few seconds.

def get_user_row(username):
    df = get_sheet_df()
    for idx, row in df.iterrows():
        if row["username"] == username:
            return df, idx, row
    return df, None, None

def update_scan_count(username) -> bool:
    """Return True if user may scan, False if limit reached."""
    df, idx, row = get_user_row(username)
    today = datetime.today().strftime("%Y-%m-%d")

    if row is None:
        return False                                           # should not happen

    # reset daily count
    if str(row["last_scan_date"]) != today:
        df.at[idx, "scan_count"]     = 0
        df.at[idx, "last_scan_date"] = today

    count = int(df.at[idx, "scan_count"])
    if count >= FREE_LIMIT:
        save_df(df)
        return False                                           # limit reached

    # increment and save
    df.at[idx, "scan_count"] = count + 1
    df.at[idx, "last_scan_date"] = today
    save_df(df)
    return True

# ------------- AUTH -------------
@st.cache_data
def load_credentials():
    df = get_sheet_df()
    creds = {
        row['username']: {"name": row['name'], "password": row['password']}
        for _, row in df.iterrows()
    }
    return creds

def add_user(username, name, password_plain):
    df = get_sheet_df()
    hashed = stauth.Hasher([password_plain]).generate()[0]
    new_row = pd.DataFrame([[username, hashed, name, 0, datetime.today().strftime("%Y-%m-%d")]],
                           columns=["username","password","name","scan_count","last_scan_date"])
    df = pd.concat([df, new_row], ignore_index=True)
    save_df(df)

# ------------- UI -------------
st.set_page_config(page_title="AI CyberSafe Checker", layout="centered")
st.title("🛡️ AI CyberSafe Checker")

menu = st.sidebar.radio("Choose Action", ["Login", "Sign Up"])

if menu == "Sign Up":
    st.subheader("🔐 Create a New Account")
    full_name = st.text_input("Full Name")
    new_user  = st.text_input("Username")
    new_pass  = st.text_input("Password", type="password")
    if st.button("Create Account"):
        if full_name and new_user and new_pass:
            add_user(new_user, full_name, new_pass)
            st.success("Account created! Please go to **Login**.")
        else:
            st.warning("Fill all fields.")

else:
    creds = load_credentials()
    auth = stauth.Authenticate(creds, "cybersafe_cookie", "auth", cookie_expiry_days=1)
    name, auth_stat, username = auth.login("Login", "main")

    if auth_stat == False:
        st.error("Invalid credentials.")
    elif auth_stat == None:
        st.warning("Enter your login details.")
    else:
        auth.logout("Logout", "sidebar")
        st.sidebar.success(f"Welcome {name} 👋")

        st.markdown("Paste any suspicious message below to check if it's a scam.")
        msg = st.text_area("✉️ Message to analyze")

        if msg and st.button("🔍 Scan"):
            if update_scan_count(username):
                with st.spinner("Analyzing…"):
                    res = requests.post(API_URL, headers=headers, json={"inputs": msg}).json()[0]
                label, score = res["label"], round(res["score"]*100,2)
                if label.lower()=="phishing":
                    st.error(f"🚨 SCAM DETECTED ({score} %)")
                else:
                    st.success(f"✅ SAFE ({score} %)")
            else:
                st.warning("❌ You’ve reached today’s free-scan limit.")
                st.info("💳 Upgrade coming soon for unlimited scans."import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-phishing"
headers = {}  # Optional: add your HuggingFace token here if rate-limited

def query(payload):
    response = requests.post(API_URL, headers=headers, json={"inputs": payload})
    return response.json()[0]

st.set_page_config(page_title="AI CyberSafe Checker", layout="centered")
st.title("🛡️ AI CyberSafe Checker (Cloud Version)")

message = st.text_area("✉️ Paste the message to analyze:")
if message:
    with st.spinner("Analyzing..."):
        result = query(message)
        label = result.get("label", "")
        score = round(result.get("score", 0) * 100, 2)
        if label.lower() == "phishing":
            st.error(f"🚨 This looks like a SCAM ({score}%)")
        else:
            st.success(f"✅ Looks safe ({score}%)")
