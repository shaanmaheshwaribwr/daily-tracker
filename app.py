import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Shaan's Life OS", page_icon="🌟", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: bold;}
    .metric-card {background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

# --- CONNECT TO GOOGLE SHEETS ---
@st.cache_resource
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["service_account_info"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Shaan Daily Tracker").worksheet(sheet_name)

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4333/4333609.png", width=100)
st.sidebar.title("Shaan's Life OS 🚀")
menu = st.sidebar.radio("Go to:", ["🏠 Dashboard", "✅ Habit Tracker", "💰 Expense Manager", "📖 Journal"])

# --- TAB 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("👋 Welcome Back, Shaan!")
    st.write("Here is your life at a glance.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔥 **Consistency Streak**\n\n5 Days")
    with col2:
        st.success("💰 **Budget Status**\n\nOn Track")
    with col3:
        st.warning("⚡ **Current Mood**\n\nEnergetic")

# --- TAB 2: HABIT TRACKER ---
elif menu == "✅ Habit Tracker":
    st.header("📝 Daily Routines")
    
    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.now())
        date_str = date.strftime("%Y-%m-%d")
    with col2:
        mood = st.selectbox("How do you feel?", ["Energetic ⚡", "Happy 😊", "Neutral 😐", "Tired 😫", "Stressed 🤯"])

    tasks = {
        "Morning": ["Exercise (1 hr) 💪", "Meditation 🧘‍♀️", "Study Session 1 (3 hrs) 📚"],
        "Afternoon": ["Lunch 🥗", "Study Session 2 📖", "Allen Teaching 👩‍🏫"],
        "Evening": ["Dinner 🍲", "Study Session 3 📝", "Sleep (8 hrs) 😴"]
    }

    completed = []
    
    # Display Checkboxes
    for category, items in tasks.items():
        st.subheader(f"{category}")
        for item in items:
            if st.checkbox(item):
                completed.append(item)

    # Calculate Score
    total_tasks = sum(len(v) for v in tasks.values())
    score = int((len(completed) / total_tasks) * 100)
    st.progress(score / 100)
    st.write(f"**Daily Score:** {score}%")

    if st.button("💾 Save Habit Data"):
        try:
            sheet = get_google_sheet("Habits")
            sheet.append_row([date_str, mood, score, ", ".join(completed)])
            st.success("Saved to Google Sheet! ☁️")
        except Exception as e:
            st.error(f"Error: {e}")

# --- TAB 3: EXPENSE MANAGER ---
elif menu == "💰 Expense Manager":
    st.header("💸 Wallet & Budget")
    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        item = col1.text_input("Item Name (e.g., Coffee)")
        amount = col2.number_input("Amount (₹)", min_value=0)
        category = st.selectbox("Category", ["Food 🍔", "Travel 🚕", "Shopping 🛍️", "Bills 💡", "Other 🤷"])
        payment = st.selectbox("Payment Mode", ["UPI", "Cash", "Card"])
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            try:
                sheet = get_google_sheet("Expenses")
                date_str = datetime.now().strftime("%Y-%m-%d")
                sheet.append_row([date_str, item, category, amount, payment])
                st.success(f"Added ₹{amount} for {item}!")
            except Exception as e:
                st.error(f"Error: {e}")

    # Show Data Visualization
    st.write("---")
    st.subheader("📊 Your Spending")
    try:
        sheet = get_google_sheet("Expenses")
        data = sheet.get_all_records()
        if data:
            df = pd.DataFrame(data)
            fig = px.pie(df, values='Amount', names='Category', title='Where is your money going?')
            st.plotly_chart(fig)
        else:
            st.info("No expenses added yet.")
    except:
        st.info("Add your first expense to see the chart!")

# --- TAB 4: JOURNAL ---
elif menu == "📖 Journal":
    st.header("🧘‍♀️ Daily Reflection")
    
    with st.form("journal_form"):
        morning = st.text_area("☀️ Morning Goal: What is your main focus today?")
        gratitude = st.text_area("🙏 Gratitude: List 3 things you are thankful for.")
        evening = st.text_area("🌙 Evening Reflection: What went well? What can be better?")
        
        if st.form_submit_button("Save Journal Entry"):
            try:
                sheet = get_google_sheet("Journal")
                date_str = datetime.now().strftime("%Y-%m-%d")
                sheet.append_row([date_str, morning, gratitude, evening])
                st.success("Journal Entry Saved! ✍️")
            except Exception as e:
                st.error(f"Error: {e}")

