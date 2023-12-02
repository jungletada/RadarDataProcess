from datetime import datetime
import numpy as np
import pandas as pd
from path_configs import dates_selection, filter_path
from utils_read import data_mkdir


def convert_to_datetime(timestamp):
    # Function to convert string to datetime
    return datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')


def truncate_to_second(timestamp):
    return timestamp.split('.')[0] if '.' in timestamp else timestamp


def remove_duplicate_lwc(data, save_path):
    # Process column names
    original_columns = data.columns[1:]
    # Process column names to truncate the timestamps to the second level
    truncated_columns = [truncate_to_second(col) for col in original_columns]
    # Check for duplicates and keep the first occurrence
    unique_columns, index = np.unique(truncated_columns, return_index=True)
    filtered_data = data.iloc[:, index]
    # Save the filtered data to a new CSV file
    filtered_data.columns = [truncate_to_second(col) for col in filtered_data.columns]
    filtered_data.to_csv(save_path, index=False)
    num_columns = len(filtered_data.columns) - 1
    print(f"{save_path} timestamps: {num_columns}")
    return filtered_data, num_columns


def get_average(lwc_data, other_data, save_path):
    # Preparing the timestamp data for comparison
    lwc_timestamps = lwc_data.columns[1:]
    ka_band_timestamps = other_data.columns[1:]
    # Convert timestamps to datetime objects for easy comparison
    lwc_timestamps_dt = [convert_to_datetime(ts)
                         for ts in lwc_timestamps]
    other_timestamps_dt = [convert_to_datetime(truncate_to_second(ts))
                           for ts in ka_band_timestamps]

    # Dictionary to store average values for each timestamp
    average_values = {}

    # Iterate through each lwc timestamp
    for lwc_ts in lwc_timestamps_dt:
        # Find ka_band timestamps that are within 30 seconds of the lwc timestamp
        close_timestamps = [ka_ts for ka_ts in other_timestamps_dt
                            if abs((ka_ts - lwc_ts).total_seconds()) <= 120]

        # Calculate the average for each close timestamp
        if close_timestamps:
            close_timestamps_str = [ts.strftime('%Y/%m/%d %H:%M:%S') for ts in close_timestamps]
            average_values[lwc_ts.strftime('%Y/%m/%d %H:%M:%S')] = other_data[close_timestamps_str].mean(axis=1)
        else:
            raise ValueError
    # Convert the dictionary to a DataFrame
    average_values_df = pd.DataFrame(average_values)
    # Reordering the columns to match the order of lwc_data
    average_values_df = average_values_df[lwc_timestamps]
    # Inserting the 'Height' column from the original data
    average_values_df.insert(0, 'Height', lwc_data['Height'])
    # Save the result to a new CSV file
    average_values_df.to_csv(save_path, index=False)


if __name__ == '__main__':
    slim_path = 'data-slim/'
    data_mkdir(slim_path)
    data_mkdir(slim_path + 'lwc/')
    from path_configs import new_dates
    keys = ['ka_band', 'w_band', 'temperature', 'relativeHumidity', 'pressure', 'temperature']
    for key in keys:
        sum_time = 0
        data_mkdir(f'{slim_path}{key}/')
        for date_ in new_dates:
            oldfile = f'{filter_path}lwc/{date_}_lwc.csv'
            slimfile = f'{slim_path}lwc/{date_}_lwc.csv'
            df = pd.read_csv(oldfile)
            lwc_df, num_columns = remove_duplicate_lwc(df, save_path=slimfile)
            sum_time += num_columns
            # lwc_df = pd.read_csv(slimfile)
            slim_num = len(lwc_df.columns) - 1
            old_num = len(df.columns) - 1
            print("{}:{}, {}, non duplicate {:2f}%"
                  .format(date_, slim_num, old_num, slim_num / old_num * 100.0))
            other_df = pd.read_csv(f'{filter_path}{key}/{date_}_{key}.csv')
            newfile = f'{slim_path}{key}/{date_}_{key}.csv'
            get_average(lwc_df, other_df, save_path=newfile)
        print(f"Total timestamps: {sum_time}")
