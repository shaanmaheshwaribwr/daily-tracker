import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE CONFIG ---
st.set_page_config(page_title="Shaan's Life OS", page_icon="🚀")

# --- THE SMART CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # This line is the fix: It pulls the entire secret you saved
    creds_dict = dict(st.secrets["service_account_info"])
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- APP INTERFACE ---
st.title("Shaan's Life OS 🌟")
menu = st.sidebar.radio("Menu", ["✅ Habits", "💰 Expenses"])

if menu == "✅ Habits":
    st.subheader("Daily Routine")
    # Personalized for your Teaching and MBA schedule
    tasks = ["MBA Study Session 📚", "Allen Biology Class 👩‍🏫", "Meditation 🧘‍♀️", "Exercise 💪"]
    done = [task for task in tasks if st.checkbox(task)]
    
    if st.button("Save Habits"):
        try:
            sheet = get_google_sheet("Habits")
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), ", ".join(done)])
            st.success("Routine Saved to Google Sheets! ✨")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "💰 Expenses":
    st.subheader("Wallet Tracker")
    item = st.text_input("What did you buy?")
    price = st.number_input("Amount (₹)", min_value=0)
    
    if st.button("Add Expense"):
        try:
            sheet = get_google_sheet("Expenses")
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), item, price])
            st.success(f"Successfully added ₹{price} for {item}!")
        except Exception as e:
            st.error(f"Error: {e}")
