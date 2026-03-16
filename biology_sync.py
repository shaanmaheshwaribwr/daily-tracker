import gspread
import json
import os
from google.oauth2.service_account import Credentials
from datetime import datetime

# 1. Connection Setup
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ['GOOGLE_SHEETS_CREDS'])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# 2. Sheet Open Karein (Tumhara Daily Tracker)
sheet = client.open("Shaan Daily Tracker").worksheet("Biology_Teaching")

# 3. Data Entry ka Logic
def log_biology_class(batch, timing, class_level, unit, topic, hw):
    date = datetime.now().strftime("%d-%m-%Y")
    # Nayi row add ho rahi hai spreadsheet mein
    sheet.append_row([date, batch, timing, class_level, unit, topic, hw])
    print(f"Success: {topic} logged for {batch}!")

# Sample test (Isse hum baad mein automation se replace karenge)
if __name__ == "__main__":
    # Ye sirf ek example entry hai
    log_biology_class("Morning Batch", "8:00 AM", "10th", "Life Processes", "Nutrition", "Yes")
