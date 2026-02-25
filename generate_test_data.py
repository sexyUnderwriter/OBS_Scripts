import csv
from datetime import datetime, timedelta

def generate_sample_schedule(
    output_csv,
    start_date_str,
    start_time_str,
    num_games=5,
    game_length_minutes=2,
    pause_seconds=30
):
    # Parse start date and time
    start_dt = datetime.strptime(f"{start_date_str} {start_time_str}", "%m/%d/%Y %H:%M")
    teams = [
        "Tigers", "Cardinals", "Brewers", "Reds", "Pirates",
        "Mets", "Dodgers", "Giants", "Phillies", "Rockies"
    ]
    rows = []
    current_dt = start_dt

    for i in range(num_games):
        end_dt = current_dt + timedelta(minutes=game_length_minutes)
        row = {
            "Date": current_dt.strftime("%m/%d/%Y"),
            "Local Time": current_dt.strftime("%H:%M") if i == 0 else current_dt.strftime("%H:%M:%S"),
            "End Time": end_dt.strftime("%H:%M") if i == 0 else end_dt.strftime("%H:%M:%S"),
            "File Name": f"Cubs_vs_{teams[i % len(teams)]}_Game{i+1}"
        }
        rows.append(row)
        # Prepare for next game
        current_dt = end_dt + timedelta(seconds=pause_seconds)

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Local Time", "End Time", "File Name"])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    # Example usage:
    # python generate_sample_schedule.py
    start_date = input("Enter start date (MM/DD/YYYY): ").strip()
    start_time = input("Enter start time (HH:MM, 24-hour): ").strip()
    output_file = "2026_MLB_Schedule_Cubs_Only_TEST.csv"
    generate_sample_schedule(output_file, start_date, start_time)
    print(f"Sample schedule written to {output_file}")