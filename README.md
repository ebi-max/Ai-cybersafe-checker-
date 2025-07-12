# -------- APP MAIN FUNCTION --------
if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name} 👋")

    # ---------- SCAN LIMIT ENFORCEMENT ----------
    def get_user_row(username):
        df = pd.read_csv(SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid="))
        for i, row in df.iterrows():
            if row['username'] == username:
                return df, i, row
        return df, None, None

    def update_user_scan(username):
        df, row_index, row = get_user_row(username)
        today = datetime.today().strftime('%Y-%m-%d')

        if row is not None:
            if str(row['last_scan_date']) != today:
                df.at[row_index, 'scan_count'] = 0  # reset count
                df.at[row_index, 'last_scan_date'] = today

            count = int(df.at[row_index, 'scan_count'])
            if count >= 5:
                return False  # limit reached

            df.at[row_index, 'scan_count'] = count + 1
            df.at[row_index, 'last_scan_date'] = today
            df.to_csv("users_temp.csv", index=False)
            return True
        return False

    st.write("Paste any suspicious message below to detect scams.")
    message = st.text_area("✉️ Message to Analyze:")

    if message and st.button("🔍 Scan"):
        if update_user_scan(username):
            with st.spinner("Analyzing..."):
                response = requests.post(API_URL, headers=headers, json={"inputs": message})
                result = response.json()[0]
                label = result['label']
                score = round(result['score'] * 100, 2)

                if label.lower() == "phishing":
                    st.error(f"🚨 SCAM DETECTED ({score}%)")
                else:
                    st.success(f"✅ SAFE ({score}%)")
        else:
            st.warning("❌ You've reached your free scan limit for today.")
            st.info("💳 Upgrade to get unlimited access.")
