import streamlit as st
import pandas as pd
from datetime import datetime
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Shaan's Master OS", page_icon="💎", layout="wide")

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
    "“Discipline is the bridge between goals and accomplishment.”",
    "“Success is not final; failure is not fatal: It is the courage to continue that counts.”",
    "“Biology is the only science in which multiplication means the same thing as division.”",
    "“Your future is created by what you do today, not tomorrow.”"
]

# --- PREMIUM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    .metric-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border-left: 5px solid #00d2ff; }
    .quote-box { font-style: italic; color: #00d2ff; text-align: center; padding: 15px; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 20px; background: rgba(0,210,255,0.05); }
    .stCheckbox { background: rgba(255,255,255,0.03); border-radius: 8px; padding: 5px 10px; margin-bottom: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & PROFILE ---
st.sidebar.markdown("<h2 style='text-align: center;'>SHAAN OS</h2>", unsafe_allow_html=True)
st.sidebar.image("https://i.imgur.com/8K5M8vS.png", width=180) # Link to your provided photo
menu = st.sidebar.radio("COMMAND CENTER", ["📊 Executive Dashboard", "📝 Precision Routine", "💰 Expense Ledger", "📓 Daily Journal"])

# --- TAB 1: EXECUTIVE DASHBOARD ---
if menu == "📊 Executive Dashboard":
    st.title("🏛️ Executive Command Center")
    st.markdown(f"<div class='quote-box'>{random.choice(quotes)}</div>", unsafe_allow_html=True)
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Consistency", "98%", "🔥")
    c2.metric("MBA Goals", "On Track", "📚")
    c3.metric("Teaching Status", "Active", "🧬")
    c4.metric("Wallet", "Balanced", "⚖️")

    st.divider()
    
    # Financial Analytics
    try:
        df = pd.DataFrame(get_google_sheet("Expenses").get_all_records())
        if not df.empty:
            df['Amount (₹)'] = pd.to_numeric(df['Amount (₹)'], errors='coerce')
            col_left, col_right = st.columns(2)
            with col_left:
                st.subheader("Monthly Spend Distribution")
                fig = px.pie(df, values='Amount (₹)', names='Category', hole=0.6, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Cyan)
                st.plotly_chart(fig, use_container_width=True)
            with col_right:
                st.subheader("Payment Trends")
                fig2 = px.bar(df, x="Mode", y="Amount (₹)", color="Category", template="plotly_dark", barmode="group")
                st.plotly_chart(fig2, use_container_width=True)
    except:
        st.info("Analytics will populate as you log expenses.")

# --- TAB 2: PRECISION ROUTINE (WITH YOUR EXACT TIMINGS) ---
elif menu == "📝 Precision Routine":
    st.title("🎯 Detailed Daily Execution")
    st.write(f"Status for: {datetime.now().strftime('%A, %d %B %Y')}")
    
    col_morning, col_afternoon = st.columns(2)
    
    with col_morning:
        st.subheader("🌅 Early Morning Rituals")
        r1 = st.checkbox("06:00 - 06:30 | Wake Up, Freshen Up & Hydrate 💧")
        r2 = st.checkbox("06:30 - 07:00 | Exercise Session 💪")
        r3 = st.checkbox("07:00 - 07:30 | Healthy Breakfast 🍳")
        r4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏")
        r5 = st.checkbox("08:00 - 11:30 | Deep Study Block 1 (3.5 Hrs) 📚")
        
    with col_afternoon:
        st.subheader("☀️ Mid-Day & Evening")
        r6 = st.checkbox("11:30 - 12:00 | Balanced Lunch 🥗")
        r7 = st.checkbox("12:00 - 12:30 | Mindful Walk 🚶‍♀️")
        r8 = st.checkbox("12:30 - 01:00 | Power Rest 😴")
        r9 = st.checkbox("01:00 - 03:30 | Deep Study Block 2 (2.5 Hrs) 📖")
        r10 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 👩‍🏫")
        r11 = st.checkbox("08:00 - 10:30 | Dinner & Final Review 📝")
        r12 = st.checkbox("11:00 PM | Sleep (Recovery) 🌙")

    if st.button("🚀 SYNC PERFORMANCE TO CLOUD"):
        try:
            sheet = get_google_sheet("Habits")
            score = sum([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), f"{score}/12", "Sync Successful"])
            st.balloons()
            st.success(f"Excellent! You completed {score} major milestones today. ✅")
        except Exception as e: st.error(f"Sync Error: {e}")

# --- TAB 3: EXPENSE LEDGER ---
elif menu == "💰 Expense Ledger":
    st.title("💸 Advanced Financial Tracking")
    with st.form("expense_form"):
        item = st.text_input("Transaction Detail")
        amt = st.number_input("Amount (₹)", min_value=0)
        mode = st.radio("Payment Mode", ["UPI", "Cash", "Card"], horizontal=True)
        cat = st.selectbox("Category", ["Food", "Travel", "MBA/Academic", "Skincare", "Other"])
        if st.form_submit_button("Confirm Entry"):
            try:
                get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                st.success("Transaction recorded in Sheets! ✅")
            except Exception as e: st.error(f"Error: {e}")

# --- TAB 4: DAILY JOURNAL ---
elif menu == "📓 Daily Journal":
    st.title("📓 Shaan's Reflections")
    entry = st.text_area("What was the highlight of your MBA studies or Biology classes today?")
    if st.button("🔒 Secure Entry"):
        try:
            get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d %H:%M"), entry])
            st.success("Your reflection has been safely archived. 📖")
        except Exception as e: st.error(f"Error: {e}")
            
