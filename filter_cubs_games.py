import csv

def make_linux_filename(date_str, game_desc, away, home, time_ct):
    # Date: YYYYMMDD
    date_fmt = date_str.replace('/', '')
    # Opponent: if Cubs is home, opponent is away; if Cubs is away, opponent is home
    if 'Cubs' in home:
        opponent = away
    else:
        opponent = home
    # Remove spaces, special chars from opponent
    opponent_fmt = ''.join(c for c in opponent if c.isalnum())
    # Time: HHMM
    time_fmt = time_ct.replace(':', '')
    # Compose filename
    return f"{date_fmt}_{opponent_fmt}_{time_fmt}.mkv"

def filter_cubs_games(input_csv, output_csv):
    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        new_header = header + ['File Name']
        writer.writerow(new_header)
        for row in reader:
            # 'Game Description' is at index 7 after new columns added
            if 'Cubs' in row[7]:
                date_str = row[0]
                time_ct = row[4]
                away = row[8]
                home = row[9]
                file_name = make_linux_filename(date_str, row[7], away, home, time_ct)
                writer.writerow(row + [file_name])

if __name__ == "__main__":
    filter_cubs_games('2026_MLB_Schedule_With_CT.csv', '2026_MLB_Schedule_Cubs_Only.csv')