import csv
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from obswebsocket import obsws, requests

# Load variables from the .env file
load_dotenv()

# Pull credentials from environment
HOST = os.getenv("OBS_WS_HOST", "localhost")
PORT = int(os.getenv("OBS_WS_PORT", 4455))
PASSWORD = os.getenv("OBS_WS_PASSWORD")

def run_scheduler(csv_file):
    if not PASSWORD:
        print("Error: OBS_WS_PASSWORD not found in environment or .env file.")
        return

    ws = obsws(HOST, PORT, PASSWORD)
    
    try:
        ws.connect()
        print(f"Connected to OBS at {HOST}:{PORT}")
    except Exception as e:
        print(f"Failed to connect to OBS: {e}")
        return

    try:
        while True:
            now = datetime.now()
            
            with open(csv_file, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    start = datetime.strptime(row['Date'] + ' ' + row['Local Time'], '%m/%d/%Y %H:%M')
                    end = datetime.strptime(row['Date'] + ' ' + row['End Time'], '%m/%d/%Y %H:%M')
                    
                    # Logic to Start Recording
                    if start.strftime('%Y-%m-%d %H:%M') == now.strftime('%Y-%m-%d %H:%M'):
                        ws.call(requests.SetProfileParameter(
                            parameterCategory="Output", 
                            parameterName="RecFilenameFormatting", 
                            parameterValue=row['File Name']
                        ))
                        ws.call(requests.StartRecord())
                        print(f"[{now}] Start: {row['File Name']}")
                    
                    # Logic to Stop Recording
                    if end.strftime('%Y-%m-%d %H:%M') == now.strftime('%Y-%m-%d %H:%M'):
                        ws.call(requests.StopRecord())
                        print(f"[{now}] Stop: {row['File Name']}")
            
            # Wait 30 seconds before next check to avoid double-triggering in the same minute
            time.sleep(30) 
            
    except KeyboardInterrupt:
        print("Shutting down scheduler...")
        ws.disconnect()

if __name__ == "__main__":
    # Ensure the CSV exists before starting
    csv_path = '2026_MLB_Schedule_Cubs_Only.csv'
    if os.path.exists(csv_path):
        run_scheduler(csv_path)
    else:
        print(f"Error: {csv_path} not found.")