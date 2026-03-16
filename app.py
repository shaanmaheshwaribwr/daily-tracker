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

# --- SIDEBAR (Complete Aesthetic Icons) ---
st.sidebar.title("🌈 Shaan's Universe")
menu = st.sidebar.radio("COMMAND CENTER", [
    "🏠 Home & Vibe", 
    "⏰ Master Routine", 
    "🧬 Allen & MBA Pro", 
    "💸 Money Magic", 
    "✍️ Heart Journal"
])

# --- TAB 1: SHAAN OS DASHBOARD (UI REFILL) ---
if menu == "🏠 Home & Vibe":
    # Deep Dark UI Styles
    st.markdown("""
        <style>
        .main { background-color: #0E1117; color: #E0E0E0; }
        div[data-testid="metric-container"] {
            background-color: #1A1C23;
            border: 1px solid #3E4251;
            padding: 20px;
            border-radius: 20px;
        }
        .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00C9FF, #92FE9D); }
        </style>
    """, unsafe_allow_html=True)

    # Header section with Date & Professional Vibe
    st.markdown(f"### 🚀 SHAAN OS v2.0")
    st.caption(f"Status: Operational | {datetime.now().strftime('%A, %b %d %Y')}")
    
    # Motivation Card
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 25px; border-radius: 20px; border-left: 10px solid #00C9FF; margin-bottom: 25px;">
            <h4 style="margin:0; color: white;">"Efficiency is doing things right; Effectiveness is doing the right things."</h4>
            <p style="color: #A0A0A0; font-style: italic; margin-top: 10px;">Keep pushing, Shaan.</p>
        </div>
    """, unsafe_allow_html=True)

    # Core Stats Dashboard
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("🧬 Allen Faculty", "Grade 9-10") #
    col_stat2.metric("📊 MBA Focus", "Ops & Data Sci") #
    col_stat3.metric("💰 Monthly Budget", "₹ 80,000") #

    st.markdown("---")
    
    # Visual Routine Tracker
    st.write("📈 **Daily Progress Overview**")
    try:
        # We calculate progress based on your Habits sheet
        habits_df = pd.DataFrame(get_google_sheet("Habits").get_all_records())
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_score = habits_df[habits_df['Date'] == today_str]
        
        if not today_score.empty:
            score_val = int(today_score.iloc[0]['Score'].split('/')[0])
            progress_percent = (score_val / 12)
            st.progress(progress_percent)
            st.write(f"Currently at **{int(progress_percent * 100)}%** of your daily potential.")
        else:
            st.progress(0.0)
            st.write("Start your routine to see your progress move!")
    except:
        st.progress(0.0)

# --- TAB 2: MASTER ROUTINE (STYLIZED CHECKLIST) ---
elif menu == "⏰ Master Routine":
    st.markdown("<h2 style='text-align: center;'>🎯 Precision Routine Center</h2>", unsafe_allow_html=True)
    
    # Keeping your 12-step routine intact as requested
    today = datetime.now().strftime('%Y-%m-%d')
    if "last_date" not in st.session_state or st.session_state.last_date != today:
        st.session_state.last_date = today
        for i in range(1, 13): st.session_state[f"task_{i}"] = False

    # Styled Containers for Morning/Evening
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("<div style='background-color: #1A1C23; padding: 20px; border-radius: 15px; border: 1px solid #00C9FF;'>", unsafe_allow_html=True)
        st.subheader("🌅 Morning Flow")
        r1 = st.checkbox("06:00 - 06:30 | Wake Up & Hydrate 💧", key="task_1")
        r2 = st.checkbox("06:30 - 07:00 | Exercise Session 💪", key="task_2")
        r3 = st.checkbox("07:00 - 07:30 | Healthy Breakfast 🍳", key="task_3")
        r4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏", key="task_4")
        r5 = st.checkbox("08:00 - 11:30 | MBA Study Block 1 📚", key="task_5")
        r6 = st.checkbox("11:30 - 12:00 | Balanced Lunch 🥗", key="task_6")
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div style='background-color: #1A1C23; padding: 20px; border-radius: 15px; border: 1px solid #92FE9D;'>", unsafe_allow_html=True)
        st.subheader("☀️ Evening Flow")
        r7 = st.checkbox("12:00 - 12:30 | Mindful Walk 🚶‍♀️", key="task_7")
        r8 = st.checkbox("12:30 - 01:00 | Power Rest/Nap 😴", key="task_8")
        r9 = st.checkbox("01:00 - 03:30 | MBA Study Block 2 📖", key="task_9")
        r10 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 🧬", key="task_10")
        r11 = st.checkbox("08:00 - 10:30 | Dinner & Review 📝", key="task_11")
        r12 = st.checkbox("11:00 PM | Dreamland 🌙", key="task_12")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 SYNC DAY TO GOOGLE SHEETS"):
        try:
            sheet = get_google_sheet("Habits")
            score = sum([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
            sheet.append_row([today, f"{score}/12", "Operational"])
            st.balloons()
            st.success(f"System Updated: {score}/12 cycles completed! 🔥")
        except:
            st.error("Connection Error: Check your Sheets tab 'Habits'.")

# --- TAB 2: MASTER ROUTINE (Full 12 Steps) ---
elif menu == "⏰ Master Routine":
    st.title("🎯 Precision Timetable 🌸")
    today = datetime.now().strftime('%Y-%m-%d')
    if "last_date" not in st.session_state or st.session_state.last_date != today:
        st.session_state.last_date = today
        for i in range(1, 13): st.session_state[f"task_{i}"] = False

    colA, colB = st.columns(2)
    with colA:
        st.markdown("### 🌅 Morning Flow")
        r1 = st.checkbox("06:00 - 06:30 | Wake Up & Hydrate 💧", key="task_1")
        r2 = st.checkbox("06:30 - 07:00 | Exercise Session 💪", key="task_2")
        r3 = st.checkbox("07:00 - 07:30 | Healthy Breakfast 🍳", key="task_3")
        r4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏", key="task_4")
        r5 = st.checkbox("08:00 - 11:30 | MBA Study Block 1 📚", key="task_5")
        r6 = st.checkbox("11:30 - 12:00 | Balanced Lunch 🥗", key="task_6")
    with colB:
        st.markdown("### ☀️ Evening Flow")
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

# --- TAB 3: ALLEN & MBA PRO (100% ACCURATE & WORKING) ---
elif menu == "🧬 Allen & MBA Pro":
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎓 Professional Task Manager</h1>", unsafe_allow_html=True)
    
    colL, colR = st.columns(2)
    
    with colL:
        st.markdown("### 🧬 Allen Biology (Grades 9 & 10)")
        bio_task = st.text_input("New Biology Lesson/Task", placeholder="e.g., Photosynthesis Quiz", key="bio_input")
        if st.button("Add Bio Task"):
            try:
                sheet = get_google_sheet("Allen_Tasks")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), bio_task, "Pending"])
                st.success("Biology task added! 🧬")
            except Exception as e:
                st.error("Tab 'Allen_Tasks' missing! Apni Google Sheet mein 'Allen_Tasks' naam ka tab banaiye.")

    with colR:
        st.markdown("### 📊 MBA Operations & Data Science")
        mba_task = st.text_input("New MBA/Data Science Task", placeholder="e.g., Linear Regression Study", key="mba_input")
        if st.button("Add MBA Task"):
            try:
                sheet = get_google_sheet("MBA_Tasks")
                sheet.append_row([datetime.now().strftime("%Y-%m-%d"), mba_task, "Pending"])
                st.success("MBA task added! 📊")
            except Exception as e:
                st.error("Tab 'MBA_Tasks' missing! Apni Google Sheet mein 'MBA_Tasks' naam ka tab banaiye.")

    st.markdown("---")
    st.subheader("📋 Recent Professional Tasks")
    
    # Display tables only if tabs exist
    try:
        st.write("**Recent Allen Bio:**")
        bio_data = pd.DataFrame(get_google_sheet("Allen_Tasks").get_all_records())
        if not bio_data.empty: st.table(bio_data.tail(3))
        
        st.write("**Recent MBA Tasks:**")
        mba_data = pd.DataFrame(get_google_sheet("MBA_Tasks").get_all_records())
        if not mba_data.empty: st.table(mba_data.tail(3))
    except:
        st.info("Tasks yahan dikhenge jab aap naye sheets tab bana lenge! 🚀")

# --- TAB 4: MONEY MAGIC (ADVANCED) ---
elif menu == "💸 Money Magic":
    st.title("💰 Advanced Wallet Tracker 💸")
    with st.expander("➕ Log New Expense", expanded=True):
        with st.form("money_form"):
            col1, col2 = st.columns(2)
            with col1:
                item = st.text_input("Item 🛍️")
                amt = st.number_input("Amount (₹)", min_value=0)
            with col2:
                cat = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA/Books 📚", "Hostel 🏠", "Others"])
                mode = st.radio("Mode", ["UPI 📱", "Cash 💵"], horizontal=True)
            if st.form_submit_button("✨ SECURELY LOG SPEND"):
                try:
                    get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                    st.balloons()
                    st.success("Logged! ✅")
                except Exception as e: st.error(f"Error: {e}")
    try:
        data = pd.DataFrame(get_google_sheet("Expenses").get_all_records())
        if not data.empty:
            st.metric("Total Spent Today", f"₹{data[data['Date'] == datetime.now().strftime('%Y-%m-%d')]['Amount'].sum()}")
            st.dataframe(data.tail(5), use_container_width=True)
    except: st.info("Analytics will show here once you log expenses.")

# --- TAB 5: HEART JOURNAL ---
elif menu == "✍️ Heart Journal":
    st.title("📓 Shaan's Reflections ✍️")
    msg = st.text_area("How are you feeling today, Shaan?")
    if st.button("🔒 SEAL ENTRY"):
        try:
            get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d"), msg])
            st.success("Memory saved safely. ❤️")
        except: st.error("Tab 'Journal' missing!")
    import json

def log_biology_local(batch, timing, class_name, topic, hw):
    new_entry = {
        "date": "16-03-2026",
        "batch": batch,
        "timing": timing,
        "class": class_name,
        "topic": topic,
        "homework": hw
    }
    
    # Purana data read karo
    with open('shaan_tracker_data.json', 'r') as f:
        data = json.load(f)
    
    # Naya data jodo
    data.append(new_entry)
    
    # Wapas save kar do
    with open('shaan_tracker_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Done! Data saved in GitHub file.")





