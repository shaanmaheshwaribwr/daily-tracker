import streamlit as st
import pandas as pd
from datetime import datetime
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Shaan's Joyful OS 🌈", page_icon="❤️", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["service_account_info"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- VIBRANT STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); border-radius: 20px; padding: 20px; border: 2px solid rgba(255,255,255,0.3); }
    .stButton>button { background: linear-gradient(45deg, #FF0080, #FF8C00); color: white; border: none; font-weight: bold; border-radius: 30px; height: 3.5em; transition: 0.5s; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .stButton>button:hover { transform: scale(1.05); filter: brightness(1.2); }
    .quote-box { font-size: 20px; font-weight: bold; color: #FFEB3B; text-shadow: 2px 2px 4px #000; text-align: center; padding: 25px; border: 3px solid #FFEB3B; border-radius: 25px; margin-bottom: 30px; }
    h1, h2, h3 { color: #FFEB3B !important; }
    .stCheckbox { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 10px; margin: 5px 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & PROFILE ---
st.sidebar.markdown("<h1 style='text-align: center; color: #FFEB3B;'>🌈 SHAAN OS</h1>", unsafe_allow_html=True)
st.sidebar.image("https://i.imgur.com/8K5M8vS.png", width=200) # Your beautiful photo!
menu = st.sidebar.selectbox("WHERE TO NEXT? 🚀", ["🏠 Home Dashboard", "⏰ My Master Timetable", "💸 Money Magic", "✍️ Heartfelt Journal"])

# --- QUOTES LIST ---
quotes = [
    "✨ 'Do what you love, and you'll never work a day in your life!'",
    "💖 'You are capable of amazing things, Shaan!'",
    "🎓 'Education is the most powerful weapon to change the world.'",
    "🧬 'In the world of Biology, you are the ultimate evolution!'",
    "🚀 'Shoot for the moon; even if you miss, you'll land among the stars!'"
]

# --- TAB 1: JOYFUL DASHBOARD ---
if menu == "🏠 Home Dashboard":
    st.title("☀️ Good Morning, Shaan! ❤️")
    st.markdown(f"<div class='quote-box'>{random.choice(quotes)}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("🔥 Daily Streak", "12 Days", "+1")
    with col2: st.metric("📚 MBA Focus", "100%", "Great!")
    with col3: st.metric("💰 Savings", "₹2,500", "Saving up!")

    st.divider()
    
    # Visual Analytics
    try:
        df = pd.DataFrame(get_google_sheet("Expenses").get_all_records())
        if not df.empty:
            st.subheader("📊 Your Spending Joy-Chart")
            fig = px.sunburst(df, path=['Category', 'Mode'], values='Amount (₹)', color_continuous_scale='RdBu', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Add some magic (data) to see your charts! ✨")

# --- TAB 2: MASTER TIMETABLE (YOUR EXACT TIMES) ---
elif menu == "⏰ My Master Timetable":
    st.title("🎯 Precision Routine 🌸")
    st.write(f"📅 Today's Date: {datetime.now().strftime('%B %d, %Y')}")
    
    left, right = st.columns(2)
    
    with left:
        st.subheader("🌅 Rise & Shine")
        c1 = st.checkbox("06:00 - 06:30 | Wake Up & Hydrate! 💧")
        c2 = st.checkbox("06:30 - 07:00 | Exercise & Glow 💪✨")
        c3 = st.checkbox("07:00 - 07:30 | Yummy Breakfast 🍳🍓")
        c4 = st.checkbox("07:30 - 08:00 | Bath & Pooja 🙏🌸")
        c5 = st.checkbox("08:00 - 11:30 | Deep MBA Study Block 1 📚🎓")
        
    with right:
        st.subheader("🌙 Afternoon & Beyond")
        c6 = st.checkbox("11:30 - 12:00 | Healthy Lunch 🥗")
        c7 = st.checkbox("12:00 - 12:30 | Fresh Air Walk 🚶‍♀️🍃")
        c8 = st.checkbox("12:30 - 01:00 | Power Nap 😴")
        c9 = st.checkbox("01:00 - 03:30 | Study Block 2 📖⚡")
        c10 = st.checkbox("04:00 - 07:00 | Allen Biology Teaching 🧬👩‍🏫")
        c11 = st.checkbox("08:00 - 10:30 | Dinner & Relax 🍜🎬")
        c12 = st.checkbox("11:00 PM | Dreamland 🌙💤")

    if st.button("💖 SAVE MY PROGRESS"):
        try:
            sheet = get_google_sheet("Habits")
            score = sum([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12])
            sheet.append_row([datetime.now().strftime("%Y-%m-%d"), f"{score}/12", "Joyfully Completed!"])
            st.balloons()
            st.success(f"Amazing work today! You nailed {score} tasks! 🎉❤️")
        except Exception as e: st.error(f"Oops! {e}")

# --- TAB 3: MONEY MAGIC ---
elif menu == "💸 Money Magic":
    st.title("💰 Wallet Tracker 💸")
    with st.container():
        item = st.text_input("What did you spend on? 🛍️")
        amt = st.number_input("How much? (₹)", min_value=0)
        
        c1, c2 = st.columns(2)
        mode = c1.selectbox("How did you pay? 💳", ["UPI (GPay/PhonePe) 📱", "Cash 💵", "Debit Card 💳"])
        cat = c2.selectbox("What category? 🏷️", ["Food 🍔", "Travel 🚕", "MBA/Books 📚", "Beauty 💄", "Gifts 🎁"])
        
        if st.button("✨ LOG TRANSACTION"):
            try:
                get_google_sheet("Expenses").append_row([datetime.now().strftime("%Y-%m-%d"), item, cat, amt, mode])
                st.snow()
                st.success("Successfully added to your magic ledger! ✅💸")
            except Exception as e: st.error(f"Error: {e}")

# --- TAB 4: JOURNAL ---
elif menu == "✍️ Heartfelt Journal":
    st.title("📓 Daily Reflections ✍️")
    msg = st.text_area("Write down your favorite moment from today... ❤️")
    if st.button("🔒 SEAL MY DIARY"):
        try:
            get_google_sheet("Journal").append_row([datetime.now().strftime("%Y-%m-%d %H:%M"), msg])
            st.success("Your memories are safely stored! 📖✨")
        except Exception as e: st.error(f"Error: {e}")
