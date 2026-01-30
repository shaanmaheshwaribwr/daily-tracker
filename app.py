import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Shaan's Life OS", page_icon="🚀", layout="wide")

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # This uses your saved secret name
    creds_dict = dict(st.secrets["service_account_info"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- SIDEBAR NAVIGATION (RESTORED) ---
st.sidebar.title("Shaan's Life OS 🚀")
menu = st.sidebar.radio("Go to:", ["🏠 Dashboard", "✅ Habit Tracker", "💰 Expense Manager", "📖 Journal"])

# --- TAB 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("👋 Welcome Back, Shaan!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 Consistency Streak", "5 Days")
    with col2:
        st.metric("💰 Budget Status", "On Track")
    with col3:
        st.metric("✨ Current Mood", "Energetic")

# --- TAB 2: HABIT TRACKER ---
elif menu == "✅ Habit Tracker":
    st.header("📝 Daily Routines")
    date_str = st.date_input("Date", datetime.now()).strftime("%Y-%m-%d")
    mood = st.selectbox("Mood", ["Energetic ⚡", "Happy 😊", "Neutral 😐", "Tired 😫"])
    
    st.subheader("Morning")
    h1 = st.checkbox("Meditation 🧘‍♀️")
    h2 = st.checkbox("Study Session 1 (3 hrs) 📚")
    
    st.subheader("Afternoon")
    h3 = st.checkbox("Lunch 🥗")
    h4 = st.checkbox("Study Session 2 📖")
    h5 = st.checkbox("Allen Teaching 👩‍🏫")
    
    if st.button("💾 Save Habit Data"):
        try:
            sheet = get_google_sheet("Habits")
            done = [h for h in [h1,h2,h3,h4,h5] if h]
            sheet.append_row([date_str, mood, len(done), "Daily Update"])
            st.success("Routine Saved! ✅")
        except Exception as e:
            st.error(f"Error: {e}")

# --- TAB 3: EXPENSE MANAGER ---
elif menu == "💰 Expense Manager":
    st.header("💸 Wallet & Budget")
    with st.form("expense_form"):
        item = st.text_input("Item Name")
        amount = st.number_input("Amount (₹)", min_value=0)
        category = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "Bills 💡", "Shopping 🛍️"])
        if st.form_submit_button("Add Expense"):
            try:
                sheet = get_google_sheet("Expenses")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), item, category, amount])
                st.success(f"Added ₹{amount} for {item}! 💳")
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 4: JOURNAL ---
elif menu == "📖 Journal":
    st.header("🧘‍♀️ Daily Reflection")
    with st.form("journal"):
        entry = st.text_area("What's on your mind today?")
        if st.form_submit_button("Save Entry"):
            try:
                sheet = get_google_sheet("Journal")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), entry])
                st.success("Journal entry saved! 📖")
            except Exception as e:
                st.error(f"Error: {e}")
