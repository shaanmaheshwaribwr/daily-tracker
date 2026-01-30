import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- ADVANCED PAGE SETUP ---
st.set_page_config(page_title="Shaan's Premium Life OS", page_icon="💎", layout="wide")

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["service_account_info"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- PREMIUM CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }
    .stButton>button { background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; border: none; font-weight: bold; border-radius: 12px; transition: 0.3s; width: 100%; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,198,255,0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h1 style='text-align: center; color: #00c6ff;'>SHAAN OS</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("NAVIGATE", ["🏠 Dashboard", "✅ Daily Routines", "💰 Expense Manager", "📖 Daily Journal"])

# --- TAB 1: DASHBOARD (WITH CHARTS) ---
if menu == "🏠 Dashboard":
    st.title("📊 Personal Analytics Center")
    
    # 1. Fetch Expense Data for Charts
    try:
        exp_sheet = get_google_sheet("Expenses")
        data = exp_sheet.get_all_records()
        df = pd.DataFrame(data)
        
        if not df.empty:
            df['Amount'] = pd.to_numeric(df['Amount (₹)'], errors='coerce')
            total_spend = df['Amount'].sum()
            
            # Top Row Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Monthly Spend", f"₹{total_spend:,.0f}", "Financials")
            col2.metric("MBA Progress", "85%", "Academic")
            col3.metric("Routine Score", "High", "Consistency")
            
            st.divider()
            
            # 2. Charts Section
            char_col1, char_col2 = st.columns(2)
            
            with char_col1:
                st.subheader("🍕 Spending by Category")
                fig_pie = px.pie(df, values='Amount', names='Category', 
                                 hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with char_col2:
                st.subheader("📈 Spending Trend (Last 7 Days)")
                df['Date'] = pd.to_datetime(df['Date'])
                daily_trend = df.groupby('Date')['Amount'].sum().reset_index()
                fig_line = px.line(daily_trend, x='Date', y='Amount', markers=True)
                fig_line.update_traces(line_color='#00c6ff', line_width=3)
                fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("No data found in Google Sheets yet. Start adding expenses to see charts!")
            
    except Exception as e:
        st.error(f"Could not load charts: {e}")

# --- TAB 2: DAILY ROUTINES (WITH TIMINGS) ---
elif menu == "✅ Daily Routines":
    st.title("🎯 Daily Execution Plan")
    st.info("Log your activities to sync with Google Sheets automatically.")
    
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("### 🌅 Morning")
        h1 = st.checkbox("Meditation 🧘‍♀️")
        h2 = st.checkbox("Study Session 1 (3 hrs) 📚")
    with colB:
        st.markdown("### ☀️ Afternoon")
        h3 = st.checkbox("Lunch 🥗")
        h4 = st.checkbox("Study Session 2 📖")
        h5 = st.checkbox("Allen Teaching 👩‍🏫")
    with colC:
        st.markdown("### 🌙 Evening")
        h6 = st.checkbox("Dinner 🍜")
        h7 = st.checkbox("Study Session 3 📝")
        h8 = st.checkbox("Sleep (8 hrs) 😴")

    if st.button("💾 SYNC ROUTINE TO CLOUD"):
        try:
            sheet = get_google_sheet("Habits")
            tasks = sum([h1, h2, h3, h4, h5, h6, h7, h8])
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), tasks, f"{tasks}/8 Done"])
            st.success("Routine backed up! ☁️")
        except Exception as e:
            st.error(f"Sync failed: {e}")

# --- TAB 3: EXPENSE MANAGER (ADVANCED) ---
elif menu == "💰 Expense Manager":
    st.title("💸 Financial Ledger")
    item = st.text_input("Expense Description")
    amount = st.number_input("Amount (₹)", min_value=0)
    c1, c2 = st.columns(2)
    category = c1.selectbox("Category", ["Food 🍔", "Travel 🚕", "MBA/Study 📚", "Beauty/Personal Care 💄", "Miscellaneous 🤷"])
    mode = c2.selectbox("Payment Mode", ["UPI (GPay/PhonePe) 📱", "Cash 💵", "Debit/Credit Card 💳"])
    
    if st.button("💰 ADD TRANSACTION"):
        try:
            sheet = get_google_sheet("Expenses")
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), item, category, amount, mode])
            st.success(f"Successfully Logged! ✅")
        except Exception as e:
            st.error(f"Error: {e}")

# --- TAB 4: JOURNAL ---
elif menu == "📖 Daily Journal":
    st.title("📖 Personal Journal")
    entry = st.text_area("Write down your thoughts...")
    if st.button("🔒 SAVE ENTRY"):
        try:
            sheet = get_google_sheet("Journal")
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), entry])
            st.success("Entry locked in your database. ☁️")
        except Exception as e:
            st.error(f"Error: {e}")
            
