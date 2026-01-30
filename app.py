import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Shaan's Pro Tracker", page_icon="💪")
st.title("🚀 Shaan's Daily Routine & Mood Tracker")

# --- ADMIN LOGIN (SIDEBAR) ---
st.sidebar.header("🔒 Admin Login")
password = st.sidebar.text_input("Enter Password to Edit:", type="password")

# --- DATA FILE NAME ---
file_name = "shaan_tracker_data.csv"

# --- TASKS LIST ---
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

# --- VIEW MODE (For Everyone) ---
# Load data to show graph
if os.path.exists(file_name):
    history_df = pd.read_csv(file_name)
    
    # Calculate streaks or stats
    st.write("### 📊 Shaan's Consistency Score")
    st.line_chart(history_df.set_index("Date")["Score_Percent"])
else:
    st.info("No data available yet.")

# --- EDIT MODE (Only if Password is Correct) ---
if password == "Shaan123":  # <--- YOUR SECRET PASSWORD
    st.success("🔓 Unlocked! You can now edit.")
    
    st.write("---")
    st.header("📝 Update Today's Data")
    
    col1, col2 = st.columns(2)
    with col1:
        today = datetime.now().strftime('%Y-%m-%d')
        st.write(f"**Date:** {today}")
    with col2:
        mood = st.selectbox("How do you feel?", 
                            ["Energetic ⚡", "Happy 😊", "Neutral 😐", "Tired 😫", "Stressed 🤯"])

    # Checklist
    completed_tasks = []
    for time, activity in tasks.items():
        if st.checkbox(f"**{time}** - {activity}"):
            completed_tasks.append(activity)

    # Calculate Progress
    total_tasks = len(tasks)
    completed_count = len(completed_tasks)
    if total_tasks > 0:
        progress = completed_count / total_tasks
    else:
        progress = 0
    
    st.progress(progress)
    st.write(f"**Score:** {int(progress * 100)}%")

    # Save Button
    if st.button("💾 Save to Database"):
        data = {
            "Date": [today],
            "Mood": [mood],
            "Score_Percent": [int(progress * 100)],
            "Tasks_Done": [", ".join(completed_tasks)]
        }
        df = pd.DataFrame(data)
        
        if not os.path.exists(file_name):
            df.to_csv(file_name, index=False)
        else:
            df.to_csv(file_name, mode='a', header=False, index=False)
        st.success("Saved successfully!")
        st.rerun()

    # DOWNLOAD BUTTON (To keep your Excel Sheet safe)
    st.write("---")
    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            st.download_button(
                label="📥 Download Excel File",
                data=file,
                file_name="shaan_tracker_history.csv",
                mime="text/csv"
            )

else:
    # Message for Guddu/Others
    st.write("---")
    st.info("👋 Viewing Mode Only. Ask Shaan for the password to edit.")

