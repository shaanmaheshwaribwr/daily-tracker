import json
from datetime import datetime

def log_biology_class(batch, timing, class_level, unit, topic, hw):
    file_name = 'biology_data.json'
    date_today = datetime.now().strftime("%d-%m-%Y")
    
    # Nayi entry ka format
    new_entry = {
        "Batch Name": batch,
        "Timing": timing,
        "Date": date_today,
        "Class": class_level,
        "Unit": unit,
        "Topic": topic,
        "Homework": hw
    }
    
    # Data save karne ka logic
    try:
        with open(file_name, 'r+') as f:
            data = json.load(f)
            data.append(new_entry)
            f.seek(0)
            json.dump(data, f, indent=4)
        print(f"Success! {topic} saved for {batch}.")
    except Exception as e:
        print("Error saving data:", e)

# Ye line tumhari class log karegi (Example data)
log_biology_class("Evening Batch", "5:00 PM", "9th", "Tissues", "Plant Tissues", "Yes")
[
  {
    "Batch Name": "Morning Batch",
    "Timing": "8:00 AM",
    "Date": "16-03-2026",
    "Class": "10th",
    "Unit": "Life Processes",
    "Topic": "Nutrition in Plants",
    "Homework": "Diagram of Stomata"
  }
]
