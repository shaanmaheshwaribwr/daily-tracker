import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Shaan's Ultimate OS 🌈", layout="wide")

# --- DATABASE CONNECTION ---
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["shaan_os_secrets"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan_Daily_Tracker").worksheet(sheet_name)

# --- SIDEBAR ---
st.sidebar.title("🌈 Shaan's Universe")
menu = st.sidebar.radio("COMMAND CENTER", ["🏠 Home & Vibe", "⏰ Master Routine", "🧬 Allen & MBA Pro", "💸 Money Magic", "✍️ Heart Journal"])

# --- TAB 1: HOME & VIBE (PROFESSIONAL & PLAYFUL) ---
if menu == "🏠 Home & Vibe":
    quotes = ["Believe in yourself! ✨", "Biology gives you a brain. Life turns it into a mind. 🧬", "Data is the new oil! 📊", "Focus on the goal, Shaan! 🔥"]
    st.markdown(f'<div style="background: linear-gradient(to right, #FF512F, #DD2476); padding: 30px; border-radius: 20px; text-align: center; color: white;"><h1>☀️ Hello, Shaan! ❤️</h1><p>"{random.choice(quotes)}"</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🧬 Allen Bio", "Grade 9-10 Expert")
    col2.metric("📊 MBA Track", "Ops & Data Sci")
    col3.metric("💖 Mood", "Guddu Magic Active")

# --- TAB 4: MONEY MAGIC (ADVANCED WALLET) ---
elif menu == "💸 Money Magic":
    st.title("💰 Advanced Wallet Tracker 💸")
    with st.expander("➕ Log New Expense", expanded=True):
        with st.form("money_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                item = st.text_input("What did you buy? 🛍️")
                amt = st.number_input("Amount (₹)", min_value=0)
            with col_f2:
                cat = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA/Books 📚", "Hostel 🏠", "Others"])
                mode = st.radio("Mode", ["UPI 📱", "Cash 💵"], horizontal=True)
            
            if st.form_submit_button("✨ SECURELY LOG SPEND"):
                try:
                    sheet = get_google_sheet("Expenses")
                    sheet.append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                    st.balloons()
                    st.success(f"₹{amt} logged for {item}! ✅")
                except Exception as e:
                    st.error(f"Error: Make sure your Sheet has an 'Expenses' tab! {e}")

    # Analysis Section
    st.markdown("---")
    st.subheader("📊 Expense Insights")
    try:
        data = pd.DataFrame(get_google_sheet("Expenses").get_all_records())
        if not data.empty:
            st.metric("Total Spent Today", f"₹{data[data['Date'] == datetime.now().strftime('%Y-%m-%d')]['Amount'].sum()}")
            st.dataframe(data.tail(5), use_container_width=True)
    except:
        st.info("Log your first expense to see analytics here!")

# --- (Other tabs: Master Routine, Allen/MBA, Journal code should stay as before) ---
