import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Shaan's Pro Tracker", page_icon="💪")
st.title("🚀 Shaan's Daily Routine & Mood Tracker")

# --- YOUR NEW SCHEDULE ---
tasks = {
    "06:30 AM": "Exercise (1 hr) 💪",
    "07:30 AM": "Breakfast + News 📰",
    "08:00 AM": "Bath + Meditation 🧘‍♀️",
    "08:30 AM": "Study Session 1 (3 hrs) 📚",
    "11:30 AM": "Lunch 🥗",
    "12:00 PM": "Post-Lunch Walk (20 mins) 🚶‍♀️",
    "12:30 PM": "Study Session 2 (till 3:30) 📖",
    "03:30 PM": "Get Ready for Allen 🎒",
    "04:00 PM": "Allen Teaching (4-7 PM) 👩‍🏫",
    "07:00 PM": "Dinner + Walk 🍲",
    "08:00 PM": "Study Session 3 (1.5 hrs) 📝",
    "09:30 PM": "Calling / Relaxing 📞",
    "10:00 PM": "Sleep (Min 8 Hrs) 😴"
}

# --- DATE & MOOD ---
col1, col2 = st.columns(2)
with col1:
    today = datetime.now().strftime('%Y-%m-%d')
    st.header(f"📅 {today}")
with col2:
    st.header("🧠 Mood")
    mood = st.selectbox("How do you feel today?", 
                        ["Energetic ⚡", "Happy 😊", "Neutral 😐", "Tired 😫", "Stressed 🤯"])

# --- CHECKLIST ---
st.write("### ✅ Mark your wins for today:")
completed_tasks = []

for time, activity in tasks.items():
    if st.checkbox(f"**{time}** - {activity}"):
        completed_tasks.append(activity)

# --- PROGRESS BAR ---
total_tasks = len(tasks)
completed_count = len(completed_tasks)
if total_tasks > 0:
    progress = completed_count / total_tasks
else:
    progress = 0

st.write("---")
st.progress(progress)
st.write(f"**Progress:** {int(progress * 100)}% ({completed_count}/{total_tasks} tasks)")

# --- SAVE BUTTON ---
if st.button("💾 Save My Progress"):
    data = {
        "Date": [today],
        "Mood": [mood],
        "Score_Percent": [int(progress * 100)],
        "Tasks_Done": [", ".join(completed_tasks)]
    }
    df = pd.DataFrame(data)
    
    file_name = "shaan_tracker_data.csv"
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, mode='a', header=False, index=False)
    
    st.success(f"Saved! You achieved {int(progress * 100)}% today while feeling {mood}.")

# --- VISUALIZATION (DATA SCIENCE SECTION) ---
st.write("---")
st.header("📊 Your Consistency Graph")

if os.path.exists("shaan_tracker_data.csv"):
    try:
        # Load data
        history_df = pd.read_csv("shaan_tracker_data.csv")
        # Simple Line Chart
        st.line_chart(history_df.set_index("Date")["Score_Percent"])
        
        # Show Data Table
        with st.expander("See your full history data"):
            st.dataframe(history_df)
    except:
        st.error("Data file is empty or corrupted. Try saving today's progress first!")
else:
    st.info("Start saving data to see your graph here!")
