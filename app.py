import streamlit as st
import pandas as pd
from datetime import datetime
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="Shaan's Ultimate OS 🌈", page_icon="💖", layout="wide")

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["shaan_os_secrets"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan_Daily_Tracker").worksheet(sheet_name)

# --- VIBRANT CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.15); border-radius: 20px; padding: 15px; border: 1px solid rgba(255,255,255,0.2); }
    .stButton>button { background: linear-gradient(45deg, #ff9a9e, #fad0c4); color: #333; border-radius: 25px; font-weight: bold; border: none; width: 100%; height: 3em; }
    .stButton>button:hover { transform: scale(1.05); transition: 0.3s; }
    .section-box { background: rgba(0, 0, 0, 0.2); padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & VIBE ---
st.sidebar.image("https://i.imgur.com/8K5M8vS.png", width=150) 
st.sidebar.title("🌈 Shaan's Universe")
menu = st.sidebar.radio("COMMAND CENTER", ["🏠 Home & Vibe", "⏰ Master Routine", "🧬 Allen & MBA Pro", "💸 Money Magic", "✍️ Heart Journal"])

# --- TAB 1: HOME & VIBE ---
if menu == "🏠 Home & Vibe":
    st.title("☀️ Hello, Shaan! ❤️")
    with st.container():
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        colV1, colV2 = st.columns([2, 1])
        with colV1:
            vibe = st.select_slider("How is your Vibe right now?", options=["Lonely 😔", "Neutral 😐", "Productive 🔥", "Happy 😊", "Guddu Magic 💖"])
            st.write(f"Current Vibe: **{vibe}**")
        with colV2:
            if st.button("Log My Vibe"):
                st.balloons()
                st.success("Vibe Recorded! ✨")
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Relationship ❤️", "Guddu", "Special")
    c2.metric("MBA Progress 📚", "84% Grade", "Top Tier")
    c3.metric("Allen Teaching 🧬", "Grade 9 & 10", "Pro")

    st.divider()
    st.subheader("📊 Your Financial Joy-Chart")
    try:
        df = pd.DataFrame(get_google_sheet("Expenses").get_all_records())
        if not df.empty:
            fig = px.pie(df, values='Amount (₹)', names='Category', hole=0.5, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    except: st.info("Add some expenses to see the magic! ✨")

# --- TAB 2: MASTER ROUTINE (FULL 24-HOUR FLOW) ---
elif menu == "⏰ Master Routine":
    st.title("🎯 Precision Timetable 🌸")
    st.write(f"📅 Today's Date: {datetime.now().strftime('%B %d, %Y')}")
    
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("### 🌅 Morning Flow")
        r1 = st.checkbox("06:00 - 06:30 | Wake Up & Hydrate 💧")
        r2 = st.checkbox("06:30 - 07:00 | Exercise Session 💪")
        r3 = st.checkbox("07:00 - 07:30 | Healthy Breakfast 🍳")
        r4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏")
        r5 = st.checkbox("08:00 - 11:30 | MBA Study Block 1 📚")
        r6 = st.checkbox("11:30 - 12:00 | Balanced Lunch 🥗")
        
    with colB:
        st.markdown("### ☀️ Afternoon & Evening")
        r7 = st.checkbox("12:00 - 12:30 | Mindful Walk 🚶‍♀️")
        r8 = st.checkbox("12:30 - 01:00 | Power Rest/Nap 😴")
        r9 = st.checkbox("01:00 - 03:30 | MBA Study Block 2 📖")
        r10 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 🧬")
        r11 = st.checkbox("08:00 - 10:30 | Dinner & Final Review 📝")
        r12 = st.checkbox("11:00 PM | Dreamland 🌙")

    if st.button("🚀 SYNC MY DAY"):
        try:
            sheet = get_google_sheet("Habits")
            # This calculates your score out of 12 tasks
            score = sum([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), f"{score}/12", "Joyfully Completed!"])
            st.balloons()
            st.success(f"Amazing, Shaan! You completed {score}/12 tasks today! 🔥❤️")
        except Exception as e:
            st.error(f"Sync Error: {e}")

# --- TAB 3: ALLEN & MBA PRO (MODIFIED TO TO-DO LIST) ---
elif menu == "🧬 Allen & MBA Pro":
    st.title("🎓 Professional To-Do List")
    
    # Setup for temporary memory of tasks
    if 'allen_list' not in st.session_state: st.session_state.allen_list = []
    if 'mba_list' not in st.session_state: st.session_state.mba_list = []

    colL, colR = st.columns(2)
    
    with colL:
        st.header("🧬 Allen Biology (Grades 9 & 10)")
        new_bio = st.text_input("Add Bio Task", key="bio_add")
        if st.button("Add to Allen") and new_bio:
            st.session_state.allen_list.append(new_bio)
        
        for i, task in enumerate(st.session_state.allen_list):
            if st.checkbox(f"{task}", key=f"bio_{i}"):
                st.write(f"~~{task}~~ ✅")

    with colR:
        st.header("📊 MBA Operations & Data Science")
        new_mba = st.text_input("Add MBA Task", key="mba_add")
        if st.button("Add to MBA") and new_mba:
            st.session_state.mba_list.append(new_mba)
            
        for i, task in enumerate(st.session_state.mba_list):
            if st.checkbox(f"{task}", key=f"mba_{i}"):
                st.write(f"~~{task}~~ ✅")

# --- TAB 4: MONEY MAGIC ---
elif menu == "💸 Money Magic":
    st.title("💰 Wallet Tracker 💸")
    with st.form("money"):
        item = st.text_input("What did you buy? 🛍️")
        amt = st.number_input("Amount (₹)", min_value=0)
        cat = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA/Books 📚", "Beauty 💄", "Others"])
        if st.form_submit_button("✨ LOG SPEND"):
            try:
                get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, "UPI"])
                st.success("Saved! ✅")
            except Exception as e: st.error(f"Error: {e}")

# --- TAB 5: HEART JOURNAL ---
elif menu == "✍️ Heart Journal":
    st.title("📓 Shaan's Reflections ✍️")
    msg = st.text_area("Write about your day... ❤️")
    if st.button("🔒 SEAL ENTRY"):
        try:
            get_sheet = get_google_sheet("Journal")
            get_sheet.append_row([datetime.now().strftime("%Y-%m-%d"), msg])
            st.success("Memory saved safely. 📖")
        except Exception as e: st.error(f"Error: {e}")

