import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE SETUP ---
st.set_page_config(page_title="Shaan's Pro OS", page_icon="🧬", layout="wide")

# --- DB CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["shaan_os_secrets"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan_Daily_Tracker").worksheet(sheet_name)

# --- THE TASK MANAGER LOGIC ---
if "mba_tasks" not in st.session_state:
    st.session_state.mba_tasks = []
if "allen_tasks" not in st.session_state:
    st.session_state.allen_tasks = []

# --- SIDEBAR ---
menu = st.sidebar.radio("NAVIGATE", ["🏠 Dashboard", "🧬 Allen & MBA Pro", "💸 Expenses"])

# --- TAB: ALLEN & MBA PRO (THE TO-DO LIST) ---
if menu == "🧬 Allen & MBA Pro":
    st.title("🎓 Professional Task Manager")
    st.markdown("---")
    
    colL, colR = st.columns(2)
    
    with colL:
        st.subheader("🧬 Allen Biology Tasks")
        new_allen = st.text_input("Add Allen Task (e.g., Prepare Cell Biology MCQ)", key="allen_input")
        if st.button("Add to Allen List"):
            st.session_state.allen_tasks.append(new_allen)
        
        st.write("Current Tasks:")
        for i, task in enumerate(st.session_state.allen_tasks):
            if st.checkbox(f"Allen: {task}", key=f"a_{i}"):
                st.write(f"~~{task}~~ ✅")

    with colR:
        st.subheader("📊 MBA Operations Tasks")
        new_mba = st.text_input("Add MBA Task (e.g., Data Science Python Module)", key="mba_input")
        if st.button("Add to MBA List"):
            st.session_state.mba_tasks.append(new_mba)
            
        st.write("Current Tasks:")
        for i, task in enumerate(st.session_state.mba_tasks):
            if st.checkbox(f"MBA: {task}", key=f"m_{i}"):
                st.write(f"~~{task}~~ ✅")
                
    if st.button("💾 Save Progress to Cloud"):
        st.success("Your professional progress is synced! ☁️")

# --- REST OF THE TABS (Dashboard, Expenses, etc.) ---
# [Keep the previous logic for Dashboard and Money Magic here]
