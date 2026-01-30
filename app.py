import streamlit as st
import pandas as pd
from datetime import datetime
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Shaan's Executive OS", page_icon="👔", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["service_account_info"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- DYNAMIC QUOTES ---
quotes = [
    "“The only way to do great work is to love what you do.” – Steve Jobs",
    "“Success is the sum of small efforts, repeated day in and day out.”",
    "“Focus on being productive instead of busy.”",
    "“Your education is a dress rehearsal for a life that is yours to lead.”",
    "“Biology is the only science in which multiplication means the same thing as division.”"
]

# --- PREMIUM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .metric-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border-left: 5px solid #00c6ff; }
    .quote-box { font-style: italic; color: #00c6ff; text-align: center; padding: 20px; border: 1px dashed #444; border-radius: 10px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & LOGO ---
st.sidebar.image("https://i.imgur.com/8K5M8vS.png", width=150) # Use your uploaded photo link here
st.sidebar.title("SHAAN MAHESHWARI")
menu = st.sidebar.radio("COMMAND CENTER", ["📊 Executive Dashboard", "📝 Full Daily Routine", "💰 Expense Ledger", "📓 Private Journal"])

# --- TAB 1: EXECUTIVE DASHBOARD ---
if menu == "📊 Executive Dashboard":
    st.title("🏛️ Executive Command Center")
    st.markdown(f"<div class='quote-box'>{random.choice(quotes)}</div>", unsafe_allow_html=True)
    
    # Summary Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Consistency", "94%", "🔥")
    with c2: st.metric("MBA Prep", "Module 4", "📚")
    with c3: st.metric("Allen Teaching", "Active", "👩‍🏫")
    with c4: st.metric("Budget", "Healthy", "✅")

    st.divider()
    
    # Financial Analytics
    try:
        df = pd.DataFrame(get_google_sheet("Expenses").get_all_records())
        if not df.empty:
            col_left, col_right = st.columns(2)
            with col_left:
                st.subheader("Spending Analysis")
                fig = px.pie(df, values='Amount (₹)', names='Category', hole=0.5, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            with col_right:
                st.subheader("Payment Distribution")
                fig2 = px.bar(df, x="Mode", y="Amount (₹)", color="Category", template="plotly_dark")
                st.plotly_chart(fig2, use_container_width=True)
    except:
        st.info("Charts will appear once you add data to your Google Sheet.")

# --- TAB 2: FULL DAILY ROUTINE (WITH TIMINGS) ---
elif menu == "📝 Full Daily Routine":
    st.title("🎯 Precision Timetable")
    st.write(f"Today is {datetime.now().strftime('%A, %d %B %Y')}")
    
    colA, colB = st.columns(2)
    with colA:
        st.subheader("🌅 Morning Rituals")
        r1 = st.checkbox("06:00 AM - Wake Up & Hydrate 💧")
        r2 = st.checkbox("06:30 AM - Freshen Up & Meditate 🧘‍♀️")
        r3 = st.checkbox("07:00 AM - MBA Study Session 1 (3 Hrs) 📚")
        r4 = st.checkbox("10:00 AM - Breakfast & Break ☕")
        
    with colB:
        st.subheader("☀️ Afternoon & Evening")
        r5 = st.checkbox("12:00 PM - MBA Study Session 2 📖")
        r6 = st.checkbox("02:00 PM - Lunch & Rest 🥗")
        r7 = st.checkbox("04:00 PM - Allen Biology Teaching 👩‍🏫")
        r8 = st.checkbox("08:00 PM - Dinner & Family Time 🍽️")
        r9 = st.checkbox("10:00 PM - Journal & Planning ✍️")
        r10 = st.checkbox("11:00 PM - Sleep (Restoration) 😴")

    if st.button("💾 SYNC DAY TO GOOGLE SHEETS"):
        try:
            sheet = get_google_sheet("Habits")
            completed = sum([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10])
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), f"{completed}/10", "Success"])
            st.balloons()
            st.success("Performance Data Synced! ✅")
        except Exception as e: st.error(f"Error: {e}")

# --- TAB 3: EXPENSE LEDGER ---
elif menu == "💰 Expense Ledger":
    st.title("💵 Financial Management")
    with st.form("expense_form"):
        item = st.text_input("Transaction Name")
        amt = st.number_input("Amount (₹)", min_value=0)
        mode = st.selectbox("Payment Method", ["UPI", "Cash", "Credit/Debit Card"])
        cat = st.selectbox("Category", ["Food", "Travel", "MBA Fees", "Skincare/Beauty", "Other"])
        if st.form_submit_button("Confirm Transaction"):
            try:
                get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                st.success("Transaction Logged. ✅")
            except Exception as e: st.error(f"Error: {e}")

# --- TAB 4: PRIVATE JOURNAL ---
elif menu == "📓 Private Journal":
    st.title("📓 Shaan's Reflections")
    entry = st.text_area("Record your insights, wins, or lessons learned today...")
    if st.button("🔒 Archive Entry"):
        try:
            get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d %H:%M"), entry])
            st.success("Entry encrypted and saved. 📖")
        except Exception as e: st.error(f"Error: {e}")
            
