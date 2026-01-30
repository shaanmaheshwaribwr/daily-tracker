import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE CONFIG ---
st.set_page_config(page_title="Shaan's Life OS 🚀", page_icon="✨", layout="wide")

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["service_account_info"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("Shaan's Universe")
menu = st.sidebar.selectbox("Navigation", ["🏠 Dashboard", "✅ Habits", "💰 Expenses", "📖 Journal"])

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🌟 Hello Shaan! Let's conquer today.")
    c1, c2, c3 = st.columns(3)
    c1.metric("🔥 Streak", "7 Days", "+1")
    c2.metric("💳 Monthly Spend", "₹4,500", "-5%")
    c3.metric("🧠 Mood", "Productive 🚀")
    
    st.divider()
    st.subheader("Today's Priorities")
    st.write("- Complete MBA Module 1 📚")
    st.write("- Biology Notes for Grade 9 👩‍🏫")

# --- HABIT TRACKER ---
elif menu == "✅ Habits":
    st.title("🎯 Daily Routines")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌅 Morning & Afternoon")
        h1 = st.checkbox("Meditation & Yoga 🧘‍♀️")
        h2 = st.checkbox("MBA Study (3-Hr Session) 📚")
        h3 = st.checkbox("Healthy Breakfast/Lunch 🥗")
        h4 = st.checkbox("Allen Teaching Hours 👩‍🏫")
        
    with col2:
        st.subheader("🌃 Evening & Night")
        h5 = st.checkbox("Biology Content Creation 🧬")
        h6 = st.checkbox("Evening Workout 💪")
        h7 = st.checkbox("Journaling & Planning ✍️")
        h8 = st.checkbox("8 Hours Sleep 😴")

    if st.button("🚀 Log My Progress"):
        try:
            sheet = get_google_sheet("Habits")
            score = sum([h1,h2,h3,h4,h5,h6,h7,h8])
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), score, "Advanced Update"])
            st.balloons()
            st.success(f"Bravo! You completed {score}/8 habits today! 🎉")
        except Exception as e:
            st.error(f"Sync Error: {e}")

# --- EXPENSE MANAGER ---
elif menu == "💰 Expenses":
    st.title("💸 Advanced Wallet Tracker")
    with st.form("spend"):
        item = st.text_input("Item/Service Name")
        amt = st.number_input("Amount (₹)", min_value=0)
        mode = st.radio("Payment Mode", ["UPI (GPay/PhonePe) 📱", "Cash 💵", "Debit/Credit Card 💳"], horizontal=True)
        cat = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA Fees/Books 📚", "Beauty/Skincare 💄", "Others 🤷"])
        
        if st.form_submit_button("💰 Add to Ledger"):
            try:
                sheet = get_google_sheet("Expenses")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                st.success(f"Logged: ₹{amt} via {mode} ✅")
            except Exception as e:
                st.error(f"Sync Error: {e}")

# --- JOURNAL ---
elif menu == "📖 Journal":
    st.title("💭 Personal Reflections")
    msg = st.text_area("How was your day? (MBA updates, Allen teaching highlights, personal thoughts...)")
    if st.button("🔒 Lock Journal Entry"):
        try:
            sheet = get_google_sheet("Journal")
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), msg])
            st.success("Your thoughts are safely stored in your Google Sheet. 📖")
        except Exception as e:
            st.error(f"Sync Error: {e}")

