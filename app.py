import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Shaan's Life OS", page_icon="🌟", layout="wide")

# --- CONNECT TO GOOGLE SHEETS ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # FIXED: This now correctly opens your "service_account_info" secret
    creds_dict = dict(st.secrets["service_account_info"])
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Shaan's Life OS 🚀")
menu = st.sidebar.radio("Go to:", ["🏠 Dashboard", "✅ Habit Tracker", "💰 Expense Manager", "📖 Journal"])

# --- TAB 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("👋 Welcome Back, Shaan!")
    st.info("🔥 **Consistency Streak:** 5 Days")

# --- TAB 2: HABIT TRACKER ---
elif menu == "✅ Habit Tracker":
    st.header("📝 Daily Routines")
    date_str = st.date_input("Date", datetime.now()).strftime("%Y-%m-%d")
    mood = st.selectbox("Mood", ["Energetic ⚡", "Happy 😊", "Neutral 😐", "Tired 😫"])
    
    # Your Personalized MBA & Teaching Tasks
    tasks = ["MBA Study 📚", "Biology Teaching 👩‍🏫", "Exercise 💪", "Meditation 🧘‍♀️"]
    completed = [task for task in tasks if st.checkbox(task)]
    
    if st.button("💾 Save Habit Data"):
        try:
            sheet = get_google_sheet("Habits")
            sheet.append_row([date_str, mood, len(completed), ", ".join(completed)])
            st.success("Saved to Sheets! ☁️")
        except Exception as e:
            st.error(f"Error: {e}")

# --- TAB 3: EXPENSE MANAGER ---
elif menu == "💰 Expense Manager":
    st.header("💸 Wallet & Budget")
    with st.form("expense_form"):
        item = st.text_input("Item Name")
        amount = st.number_input("Amount (₹)", min_value=0)
        category = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "Bills 💡", "Other 🤷"])
        if st.form_submit_button("Add Expense"):
            try:
                sheet = get_google_sheet("Expenses")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), item, category, amount])
                st.success(f"Added ₹{amount}!")
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 4: JOURNAL ---
elif menu == "📖 Journal":
    st.header("🧘‍♀️ Daily Reflection")
    with st.form("journal"):
        msg = st.text_area("What's on your mind?")
        if st.form_submit_button("Save Entry"):
            try:
                sheet = get_google_sheet("Journal")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), msg])
                st.success("Journal Saved!")
            except Exception as e:
                st.error(f"Error: {e}")
