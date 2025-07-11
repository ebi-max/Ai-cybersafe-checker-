import streamlit as st
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
