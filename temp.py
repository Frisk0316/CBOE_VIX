import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file into a DataFrame
df = pd.read_csv('sliced_data_days/2019-01-02.csv')

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
near_df.to_csv(f'sliced_data_near_and_next/2019-01-02-near.csv', index=False)
next_df.to_csv(f'sliced_data_near_and_next/2019-01-02-next.csv', index=False)
