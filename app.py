import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random  # <--- THIS WAS MISSING AND CAUSED THE ERROR

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

# --- TAB 1: HOME & VIBE (FIXED) ---
if menu == "🏠 Home & Vibe":
    quotes = [
        "Believe in yourself and you're halfway there. ✨",
        "Biology gives you a brain. Life turns it into a mind. 🧬",
        "Operations is the engine of success! 📊",
        "Stay focused, Shaan. Your empire is growing. 🔥"
    ]
    random_quote = random.choice(quotes)

    st.markdown(f"""
        <div style="background: linear-gradient(to right, #FF512F, #DD2476); padding: 30px; border-radius: 20px; text-align: center; color: white;">
            <h1 style="margin: 0;">☀️ Hello, Shaan! ❤️</h1>
            <p style="font-size: 1.2em; font-style: italic;">"{random_quote}"</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("🧬 Allen Biology", "Grade 9 & 10")
    col2.metric("📊 MBA Track", "Ops & Data Sci")
    col3.metric("💖 Mood", "Guddu Magic")

# --- TAB 2: MASTER ROUTINE ---
elif menu == "⏰ Master Routine":
    st.title("🎯 Precision Timetable 🌸")
    today = datetime.now().strftime('%Y-%m-%d')
    if "last_date" not in st.session_state or st.session_state.last_date != today:
        st.session_state.last_date = today
        for i in range(1, 13): st.session_state[f"task_{i}"] = False

    colA, colB = st.columns(2)
    with colA:
        r1 = st.checkbox("06:00 - 06:30 | Wake Up & Hydrate 💧", key="task_1")
        r2 = st.checkbox("06:30 - 07:00 | Exercise Session 💪", key="task_2")
        r3 = st.checkbox("07:00 - 07:30 | Healthy Breakfast 🍳", key="task_3")
        r4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏", key="task_4")
        r5 = st.checkbox("08:00 - 11:30 | MBA Study Block 1 📚", key="task_5")
        r6 = st.checkbox("11:30 - 12:00 | Balanced Lunch 🥗", key="task_6")
    with colB:
        r7 = st.checkbox("12:00 - 12:30 | Mindful Walk 🚶‍♀️", key="task_7")
        r8 = st.checkbox("12:30 - 01:00 | Power Rest/Nap 😴", key="task_8")
        r9 = st.checkbox("01:00 - 03:30 | MBA Study Block 2 📖", key="task_9")
        r10 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 🧬", key="task_10")
        r11 = st.checkbox("08:00 - 10:30 | Dinner & Review 📝", key="task_11")
        r12 = st.checkbox("11:00 PM | Dreamland 🌙", key="task_12")

    if st.button("🚀 SYNC MY DAY"):
        try:
            sheet = get_google_sheet("Habits")
            score = sum([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
            sheet.append_row([today, f"{score}/12", "Synced"])
            st.balloons()
            st.success(f"Perfect! {score}/12 tasks saved! 🔥")
        except Exception as e: st.error(f"Sync Error: {e}")

# --- TAB 3: ALLEN & MBA PRO ---
elif menu == "🧬 Allen & MBA Pro":
    st.title("🎓 Professional To-Do List")
    colL, colR = st.columns(2)
    with colL:
        st.header("🧬 Allen Biology")
        task_bio = st.text_input("New Bio Task")
        if st.button("Add to Allen"):
            get_google_sheet("Allen_Tasks").append_row([datetime.now().strftime("%Y-%m-%d"), task_bio, "Pending"])
            st.success("Task Added!")
    with colR:
        st.header("📊 MBA Operations")
        task_mba = st.text_input("New MBA Task")
        if st.button("Add to MBA"):
            get_google_sheet("MBA_Tasks").append_row([datetime.now().strftime("%Y-%m-%d"), task_mba, "Pending"])
            st.success("Task Added!")

# --- TAB 4: MONEY MAGIC ---
elif menu == "💸 Money Magic":
    st.title("💰 Wallet Tracker 💸")
    with st.form("money"):
        item = st.text_input("Item")
        amt = st.number_input("Amount (₹)", min_value=0)
        if st.form_submit_button("✨ LOG SPEND"):
            get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, amt])
            st.success("Logged!")

# --- TAB 5: HEART JOURNAL ---
elif menu == "✍️ Heart Journal":
    st.title("📓 Shaan's Reflections")
    msg = st.text_area("Write your heart out...")
    if st.button("🔒 SEAL ENTRY"):
        get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d"), msg])
        st.success("Saved. ❤️")
