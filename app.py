import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE SETUP ---
st.set_page_config(page_title="Shaan's Ultimate OS 🌈", layout="wide")

# --- DATABASE CONNECTION ---
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["shaan_os_secrets"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan_Daily_Tracker").worksheet(sheet_name)

# --- SIDEBAR (Exact Original Icons) ---
st.sidebar.title("🌈 Shaan's Universe")
menu = st.sidebar.radio("COMMAND CENTER", ["🏠 Home & Vibe", "⏰ Master Routine", "🧬 Allen & MBA Pro", "💸 Money Magic", "✍️ Heart Journal"])

# --- TAB 1: HOME & VIBE (PREMIUM DASHBOARD) ---
if menu == "🏠 Home & Vibe":
    # Dynamic Quotes List
    quotes = [
        "Believe in yourself and you're halfway there. ✨",
        "Your only limit is your mind. 🚀",
        "Biology gives you a brain. Life turns it into a mind. 🧬",
        "Data is the new oil, but Operations is the engine! 📊",
        "Everything is possible with a little bit of coffee and a lot of Guddu magic. ❤️"
    ]
    random_quote = random.choice(quotes)

    # Dashboard Header with Style
    st.markdown(f"""
        <div style="background: linear-gradient(to right, #FF512F, #DD2476); padding: 30px; border-radius: 20px; text-align: center; color: white; margin-bottom: 25px;">
            <h1 style="font-size: 3em; margin: 0;">☀️ Hello, Shaan! ❤️</h1>
            <p style="font-size: 1.5em; font-style: italic;">"{random_quote}"</p>
        </div>
    """, unsafe_allow_html=True)

    # Engaging Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown("<div style='background: #6a11cb; padding: 20px; border-radius: 15px; text-align: center; color: white;'><h3>🧬 Allen Pro</h3><p style='font-size: 25px;'>Grade 9 & 10 Expert</p></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown("<div style='background: #2575fc; padding: 20px; border-radius: 15px; text-align: center; color: white;'><h3>📊 MBA Track</h3><p style='font-size: 25px;'>Operations & Data</p></div>", unsafe_allow_html=True)
    with col_m3:
        st.markdown("<div style='background: #ff0844; padding: 20px; border-radius: 15px; text-align: center; color: white;'><h3>💖 Mood</h3><p style='font-size: 25px;'>Guddu Magic Active</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Vibe Graph
    st.subheader("📈 Your Productivity & Vibe Flow")
    try:
        # Fetching Habit data for the graph
        df_habits = pd.DataFrame(get_google_sheet("Habits").get_all_records())
        if not df_habits.empty:
            # Simple bar chart to show progress over time
            import plotly.express as px
            fig = px.area(df_habits.tail(7), x='Date', y='Score', 
                         title='Last 7 Days Consistency',
                         line_shape='spline', 
                         color_discrete_sequence=['#FF512F'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Log some tasks in 'Master Routine' to see your vibe graph! 🚀")
    except:
        st.warning("Connect your 'Habits' tab in Google Sheets to see your visual progress! 📊")

    # Motivational Poster Section
    st.markdown("---")
    st.markdown("### 🎨 Daily Inspiration")
    st.image("https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&q=80&w=1000", 
             caption="Stay Focused, Shaan! Your Nanded empire is growing. 🔥", use_container_width=True)

# --- TAB 2: MASTER ROUTINE (Full 12 Steps + Reset) ---
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
        st.markdown("### ☀️ Afternoon & Evening")
        r7 = st.checkbox("12:00 - 12:30 | Mindful Walk 🚶‍♀️", key="task_7")
        r8 = st.checkbox("12:30 - 01:00 | Power Rest/Nap 😴", key="task_8")
        r9 = st.checkbox("01:00 - 03:30 | MBA Study Block 2 📖", key="task_9")
        r10 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 🧬", key="task_10")
        r11 = st.checkbox("08:00 - 10:30 | Dinner & Final Review 📝", key="task_11")
        r12 = st.checkbox("11:00 PM | Dreamland 🌙", key="task_12")

    if st.button("🚀 SYNC MY DAY"):
        try:
            sheet = get_google_sheet("Habits")
            score = sum([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
            sheet.append_row([today, f"{score}/12", "Synced"])
            st.balloons()
            st.success(f"Perfect! {score}/12 tasks saved! 🔥")
        except Exception as e: st.error(f"Sync Error: {e}")

# --- TAB 3: ALLEN & MBA PRO (Restored Content) ---
elif menu == "🧬 Allen & MBA Pro":
    st.title("🎓 Professional To-Do List")
    colL, colR = st.columns(2)
    with colL:
        st.header("🧬 Allen Biology (Grades 9 & 10)")
        task_bio = st.text_input("Add Bio Task")
        if st.button("Add to Allen"):
            try:
                get_google_sheet("Allen_Tasks").append_row([datetime.now().strftime("%Y-%m-%d"), task_bio, "Pending"])
                st.success("Allen task added!")
            except: st.error("Tab 'Allen_Tasks' not found!")
    with colR:
        st.header("📊 MBA Operations & Data Science")
        task_mba = st.text_input("Add MBA Task")
        if st.button("Add to MBA"):
            try:
                get_google_sheet("MBA_Tasks").append_row([datetime.now().strftime("%Y-%m-%d"), task_mba, "Pending"])
                st.success("MBA task added!")
            except: st.error("Tab 'MBA_Tasks' not found!")

# --- TAB 4: MONEY MAGIC (Restored Working Tracker) ---
elif menu == "💸 Money Magic":
    st.title("💰 Wallet Tracker 💸")
    with st.form("money"):
        item = st.text_input("What did you buy? 🛍️")
        amt = st.number_input("Amount (₹)", min_value=0)
        mode = st.radio("Mode", ["UPI 📱", "Cash 💵"], horizontal=True)
        cat = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA/Books 📚", "Others"])
        if st.form_submit_button("✨ LOG SPEND"):
            try:
                get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                st.success("Expense logged! ✅")
            except: st.error("Tab 'Expenses' not found!")

# --- TAB 5: HEART JOURNAL (Restored) ---
elif menu == "✍️ Heart Journal":
    st.title("📓 Shaan's Reflections ✍️")
    msg = st.text_area("How are you feeling today?")
    if st.button("🔒 SEAL ENTRY"):
        try:
            get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d"), msg])
            st.success("Memory saved safely. ❤️")
        except: st.error("Tab 'Journal' not found!")

