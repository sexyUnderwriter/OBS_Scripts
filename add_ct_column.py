def add_four_hours(time_str):
    """Adds 4 hours to a time string in HH:MM format, returns as string."""
    try:
        hour, minute = map(int, time_str.split(':'))
        hour = (hour + 4) % 24
        return f"{hour:02d}:{minute:02d}"
    except Exception:
        return time_str
import csv

def subtract_one_hour(et_time):

    """Subtracts one hour from a time string in HH:MM format, returns as string."""
    try:
        hour, minute = map(int, et_time.split(':'))
        hour = (hour - 1) % 24
        return f"{hour:02d}:{minute:02d}"
    except Exception:
        return et_time

def subtract_fifteen_minutes(time_str):
    """Subtracts 15 minutes from a time string in HH:MM format, returns as string."""
    try:
        hour, minute = map(int, time_str.split(':'))
        total_minutes = hour * 60 + minute - 15
        hour = (total_minutes // 60) % 24
        minute = total_minutes % 60
        return f"{hour:02d}:{minute:02d}"
    except Exception:
        return time_str


def add_ct_start_end_time_columns(input_csv, output_csv):
    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        # Insert new columns as 5th, 6th, and 7th columns
        new_header = header[:4] + ['Time - CT', 'Start Time', 'End Time'] + header[4:]
        writer.writerow(new_header)
        for row in reader:
            et_time = row[3]
            ct_time = subtract_one_hour(et_time)
            start_time = subtract_fifteen_minutes(ct_time)
            end_time = add_four_hours(ct_time)
            new_row = row[:4] + [ct_time, start_time, end_time] + row[4:]
            writer.writerow(new_row)

if __name__ == "__main__":
    add_ct_start_end_time_columns('2026 MLB Schedule (With Times).xlsx - Sheet1.csv', '2026_MLB_Schedule_With_CT.csv')
