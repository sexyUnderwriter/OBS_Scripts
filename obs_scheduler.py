import csv
import time
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from obswebsocket import obsws, requests

# Load variables from the .env file
load_dotenv()

# Pull credentials from environment
HOST = os.getenv("OBS_WS_HOST", "localhost")
PORT = int(os.getenv("OBS_WS_PORT", 4455))
PASSWORD = os.getenv("OBS_WS_PASSWORD")

def parse_datetime(date_str, time_str):
    """Parse date and time, supporting both HH:MM and HH:MM:SS."""
    for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M"):
        try:
            return datetime.strptime(f"{date_str} {time_str}", fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{date_str} {time_str}' does not match expected formats.")

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
                    try:
                        start = parse_datetime(row['Date'], row['Local Time'])
                        end = parse_datetime(row['Date'], row['End Time'])
                    except Exception as e:
                        print(f"Skipping row due to parse error: {e}")
                        continue
                    
                    # Logic to Start Recording
                    if start.strftime('%Y-%m-%d %H:%M:%S') == now.strftime('%Y-%m-%d %H:%M:%S'):
                        ws.call(requests.SetProfileParameter(
                            parameterCategory="Output", 
                            parameterName="RecFilenameFormatting", 
                            parameterValue=row['File Name']
                        ))
                        ws.call(requests.StartRecord())
                        print(f"[{now}] Start: {row['File Name']}")
                    
                    # Logic to Stop Recording
                    if end.strftime('%Y-%m-%d %H:%M:%S') == now.strftime('%Y-%m-%d %H:%M:%S'):
                        ws.call(requests.StopRecord())
                        print(f"[{now}] Stop: {row['File Name']}")
            
            # Wait 1 second before next check for second-level precision
            time.sleep(1) 
            
    except KeyboardInterrupt:
        print("Shutting down scheduler...")
        ws.disconnect()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python obs_scheduler.py <csv_file>")
        sys.exit(1)
    csv_path = sys.argv[1]
    if os.path.exists(csv_path):
        run_scheduler(csv_path)
    else:
        print(f"Error: {csv_path} not found.")