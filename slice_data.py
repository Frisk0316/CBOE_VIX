import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file into a DataFrame
df = pd.read_csv('original_file/spx_spxw_s.csv')

# Extract unique dates from the 'date' column
unique_dates = df['date'].unique()

# Iterate over each unique date
# for date_str in unique_dates:

#     print("Writing " + date_str + ".csv ...")
#     # Slice the DataFrame for the current date
#     sliced_df = df[df['date'] == date_str]
#     # Write the sliced DataFrame to a new CSV file
#     sliced_df.to_csv(f'sliced_data_days/{date_str}.csv', index=False)


# task: for every_sliced data, catch the "exdate" and create two files: "date"-near.csv and "date"-next.csv
#       near.csv: exdate - date is nearest to 30 days
#       next.csv: next week of exdate

# example: date = 2019-01-02
#          exdate = 2019-01-25
#          nearest date = 2019-02-01

# remind: the exdate always be the friday of the week

for date_str in unique_dates:

    filename = "sliced_data_days/" + date_str + ".csv"
    df = pd.read_csv(filename)
    
    # Convert 'date' and 'exdate' columns to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    df['exdate'] = pd.to_datetime(df['exdate'])

    # Function to find the nearest exdate with days difference closest to 30 days
    def find_nearest_exdate(date, exdates):
        nearest_exdate = None
        min_diff = 23
        for exdate in exdates:
            diff = abs((date - exdate).days)
            if 0 < diff < 30 and min_diff < diff:
                min_diff = diff
                nearest_exdate = exdate
        return nearest_exdate

    # Function to find the next Friday
    def find_next_friday(date):
        while date.weekday() != 4:  # 4 represents Friday
            date += timedelta(days=1)
        return date

    # Get unique 'exdate' values for the current date
    unique_exdates = df['exdate'].unique()

    # Calculate the nearest and next exdate
    nearest_exdate = find_nearest_exdate(df['date'][0], unique_exdates)
    next_friday = find_next_friday(nearest_exdate + timedelta(days=7))

    # Filter data for near.csv and next.csv
    near_df = df[df['exdate'] == nearest_exdate]
    next_df = df[df['exdate'] == next_friday] if next_friday in unique_exdates else pd.DataFrame()

    # Write near.csv and next.csv
    near_df.to_csv(f'sliced_data_near_and_next/{date_str}-near.csv', index=False)
    next_df.to_csv(f'sliced_data_near_and_next/{date_str}-next.csv', index=False)
    print(f"Writing {date_str}-near.csv and {date_str}-next.csv ...")
