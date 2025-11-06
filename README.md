<p align="center">
  <img src="https://github.com/ebieme-bassey/ebi-max/blob/main/banner.png" alt="AI CyberSafe Checker Banner" width="100%">
</p>

# 🧠 AI CyberSafe Checker  
**Developed by:** Ebieme Bassey  
**Organization:** EBIKLEAN Integrated Services  
**Location:** Yenagoa, Bayelsa State, Nigeria  

---

## 🔍 Overview  
**AI CyberSafe Checker** is an intelligent cybersecurity tool designed to analyze and detect **phishing, scam, or fraudulent messages** using advanced Natural Language Processing (NLP).  
Built with **HuggingFace Transformers**, the app helps users identify risky content before clicking or replying.  

This project is part of the **3MTT Knowledge Showcase** under the **AI-Powered Solutions** category.  

---

## ⚙️ Key Features  
- 🚫 Detects **phishing or scam text messages** in real-time  
- 🤖 Uses **Transformer-based NLP models** for text classification  
- 📊 Provides **detailed safety analysis** (Safe / Suspicious / Dangerous)  
- 🔐 Includes **user access level verification** via Google Sheet  
- 📱 Optimized for web and Android app deployment  

---

## 💾 Tech Stack  
- **Frontend:** Streamlit / React Native  
- **Backend:** Python (Transformers, Pandas)  
- **Database:** Google Sheets (for login & premium users)  
- **Hosting:** GitHub / Streamlit Cloud  
- **Developer Tools:** GitHub Codespaces, Termux  

---

## 🔑 User Access Levels  

| Access Type | Description | Daily Scan Limit |
|--------------|-------------|------------------|
| **Free User** | Limited access for testing the tool | 3 scans per day |
| **Premium User** | Unlimited scans + advanced analysis | Unlimited |

---

## 💰 Premium Access Setup  

To upgrade your account to **Premium Access**, follow these steps:

1. **Send ₦2,000** (one-time activation fee) to  
   **Bank Name:** Fidelity Bank  
   **Account Name:** *EBIEME BASSEY*  
   **Account Number:** `6681569396`

2. **After payment**, send your:  
   - Full Name  
   - Email (used in app login)  
   - Proof of payment  

   📩 via **WhatsApp:** [Click to Chat](https://wa.me/2347031204549)

3. Your premium status will be confirmed in the Google Sheet:  
   📄 [cybersafe_users (Google Sheet)](https://docs.google.com/spreadsheets/d/1ig9XBMyz1IXwxO8qznlQJ6Wv4u21x7hkVXN0abZbBjo/edit?usp=drivesdk)

4. Once verified, your **`access_level`** will be updated to `premium` and your daily scan limit will become **unlimited**.

---

## 🧠 How It Works  

1. **User Inputs a Message:**  
   Paste any suspicious message, email, or SMS text into the input box.

2. **AI Model Analysis:**  
   The system uses a fine-tuned **Transformer model** from HuggingFace to analyze the text, detecting linguistic and contextual patterns common in scams and phishing attempts.

3. **Risk Scoring:**  
   Each message is assigned a probability score for safety and risk.  
   Based on that score, one of three verdicts is displayed:

   | Result | Description | Example |
   |---------|-------------|----------|
   | ✅ **Safe** | The message shows no signs of scam or fraud. | "Your package is ready for pickup at our office." |
   | ⚠️ **Suspicious** | The message contains partial risk indicators or unclear intent. | "Confirm your bank details to receive your reward." |
   | 🚨 **Dangerous** | The message matches known scam or phishing patterns. | "Click this link to unlock your blocked account now." |

4. **User Action Suggestion:**  
   Depending on the result, the app will show security advice such as **“Do not click any links”**, **“Report this message”**, or **“Safe to read”**.

5. **Scan Logging:**  
   Each scan is recorded in the Google Sheet with the user’s email, scan count, and last scan date to enforce free user limits.

---

## 📂 File Structure