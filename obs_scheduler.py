import csv
import time
from datetime import datetime
from obswebsocket import obsws, requests

# OBS Connection Settings
host = "localhost"
port = 4455
password = "your_password_here"

def run_scheduler(file_path):
    ws = obsws(host, port, password)
    ws.connect()
    print("Connected to OBS...")

    while True:
        now = datetime.now()
        
        with open(file_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                start = datetime.strptime(row['Start Time'], '%H:%M')
                end = datetime.strptime(row['End Time'], '%H:%M')
                
                # Check if it's time to START
                if start.strftime('%H:%M') == now.strftime('%H:%M') and start.date() == now.date():
                    # Set filename
                    ws.call(requests.SetProfileParameter(parameterCategory="Output", parameterName="RecFilenameFormatting", parameterValue=row['file_name']))
                    ws.call(requests.StartRecord())
                    print(f"Started recording: {row['File Name']}")
                
                # Check if it's time to STOP
                if end.strftime('%H:%M') == now.strftime('%H:%M') and end.date() == now.date():
                    ws.call(requests.StopRecord())
                    print(f"Stopped recording: {row['File Name']}")
        
        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    run_scheduler('2026_MLB_Schedule_Cubs_Only.csv')