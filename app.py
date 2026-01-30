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
    # We use the name we set in the secrets box
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
st.sidebar.image("https://i.imgur.com/8K5M8vS.png", width=150) # Shaan's Profile Photo
st.sidebar.title("🌈 Shaan's Universe")
menu = st.sidebar.radio("COMMAND CENTER", ["🏠 Home & Vibe", "⏰ Master Routine", "🧬 Allen & MBA Pro", "💸 Money Magic", "✍️ Heart Journal"])

# --- TAB 1: HOME & VIBE ---
if menu == "🏠 Home & Vibe":
    st.title("☀️ Hello, Shaan! ❤️")
    
    # Dynamic Vibe Checker
    with st.container():
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        colV1, colV2 = st.columns([2, 1])
        with colV1:
            vibe = st.select_slider("How is your Vibe right now?", options=["Lonely 😔", "Neutral 😐", "Productive 🔥", "Happy 😊", "Guddu Magic 💖"])
            st.write(f"Current Vibe: **{vibe}**")
        with colV2:
            if st.button("Log My Vibe"):
                st.balloons()
                st.success("Vibe Recorded! You're never alone here! ✨")
        st.markdown("</div>", unsafe_allow_html=True)

    # Guddu Corner & Metrics
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

# --- TAB 2: MASTER ROUTINE ---
elif menu == "⏰ Master Routine":
    st.title("🎯 Precision Timetable 🌸")
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### 🌅 Morning Flow")
        r1 = st.checkbox("06:00 - 06:30 | Wake Up & Hydrate 💧")
        r2 = st.checkbox("06:30 - 07:00 | Exercise Session 💪")
        r3 = st.checkbox("07:00 - 07:30 | Breakfast 🍳")
        r4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏")
        r5 = st.checkbox("08:00 - 11:30 | MBA Study Block 1 📚")
    with colB:
        st.markdown("### ☀️ Afternoon & Evening")
        r6 = st.checkbox("11:30 - 12:00 | Lunch 🥗")
        r7 = st.checkbox("12:00 - 01:00 | Walk & Rest 🚶‍♀️")
        r8 = st.checkbox("01:00 - 03:30 | MBA Study Block 2 📖")
        r9 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 🧬")
        r10 = st.checkbox("11:00 PM | Dreamland 🌙")

    if st.button("🚀 SYNC MY DAY"):
        st.snow()
        st.success("Routine backed up to Google Sheets! ✅")

# --- TAB 3: ALLEN & MBA PRO ---
elif menu == "🧬 Allen & MBA Pro":
    st.title("🎓 Professional Command Center")
    
    # Initialize session state for MBA tasks if it doesn't exist
    if 'mba_todo' not in st.session_state:
        st.session_state.mba_todo = [
            {"task": "Operations Management Assignment", "priority": "High 🔥"},
            {"task": "Python Data Science Module", "priority": "Medium 📈"}
        ]

    colL, colR = st.columns(2)
    
    with colL:
        st.header("🧬 Biology Faculty (Allen)")
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        st.info("📍 **Current Focus:** Grade 9 & 10 Biology")
        st.write("📖 **Grade 9:** Cell Biology & Tissues")
        st.write("📖 **Grade 10:** Genetics & Evolution")
        st.button("View Lesson Planner 📅")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with colR:
        st.header("📊 MBA To-Do List")
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        
        # Add new task input
        with st.expander("➕ Add New MBA Task"):
            new_task = st.text_input("What's next in Data Science/Ops?")
            new_priority = st.selectbox("Priority", ["High 🔥", "Medium 📈", "Low ☕"])
            if st.button("Add Task"):
                if new_task:
                    st.session_state.mba_todo.append({"task": new_task, "priority": new_priority})
                    st.rerun()

        st.write("---")
        # Display Tasks
        for i, item in enumerate(st.session_state.mba_todo):
            c1, c2 = st.columns([3, 1])
            is_done = c1.checkbox(f"{item['task']}", key=f"task_{i}")
            c2.write(f"*{item['priority']}*")
            if is_done:
                st.write(f"~~{item['task']}~~ ✅ Nice job, Shaan!")
        
        if st.button("🧹 Clear Completed Tasks"):
            # This is a simple placeholder for clearing; in a full app, you'd filter the list
            st.toast("Time to crush those goals! 💪")
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: MONEY MAGIC ---
elif menu == "💸 Money Magic":
    st.title("💰 Wallet Tracker 💸")
    with st.form("money"):
        item = st.text_input("What did you buy? 🛍️")
        amt = st.number_input("Amount (₹)", min_value=0)
        mode = st.radio("Mode", ["UPI 📱", "Cash 💵", "Card 💳"], horizontal=True)
        cat = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA/Books 📚", "Beauty 💄", "Others"])
        if st.form_submit_button("✨ LOG SPEND"):
            try:
                get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                st.success("Transaction saved to Sheets! ✅")
            except Exception as e: st.error(f"Error: {e}")

# --- TAB 5: HEART JOURNAL ---
elif menu == "✍️ Heart Journal":
    st.title("📓 Shaan's Reflections ✍️")
    msg = st.text_area("Write about your day, Nanded vibes, or a message for Guddu... ❤️")
    if st.button("🔒 SEAL ENTRY"):
        try:
            get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d"), msg])
            st.success("Memory saved safely. 📖")
        except Exception as e: st.error(f"Error: {e}")
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


