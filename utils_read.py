import os
import pandas as pd
from typing import List
from datetime import datetime
from dateutil import parser


def data_mkdir(directory_path):
    # 如果目录不存在，则创建目录
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)


def walk_folder(folder_path):
    file_path = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path.append(os.path.join(root, file))
    return file_path


def select_csv_from_date(csv_list, date_select):
    """
    :param csv_list:
    :param date_select:
    :return:
    """
    selected = []
    for csv in csv_list:
        if date_select in csv:
            selected.append(csv)
    if len(selected) == 0:
        raise FileNotFoundError
    return selected


def get_csv_names(csv_path):
    with open(csv_path, 'r') as file:
        path_list = file.readlines()
    path_list = [f.strip() for f in path_list]
    return path_list


def get_timestamp_from_csv(csv_paths):
    """
    Select the time stamp in  the csv file
    :param csv_paths: path to the csv file
    :return: List[datetime]
    """
    times_stamps = []
    # file = open(save_path, 'a')
    for csv_path in csv_paths:
        print(f"Dealing with {csv_path}")
        df = pd.read_csv(csv_path)
        time_strings = df.columns.tolist()[1:]
        for time_string in time_strings:
            # file.write(time_string + '\n')
            times_stamps.append(parser.parse(time_string, fuzzy=True))
    # file.close()
    return times_stamps


def find_closest_timestamp(target, timestamps, time_threshold=120):
    """
    Find the timestamp in the list that is closest to the target timestamp.
    :param time_threshold: 120s
    :param target: A datetime object representing the target timestamp
    :param timestamps: A list of datetime objects representing the timestamps to search through
    :return: The datetime object from the list that is closest to the target timestamp
    """
    closest_timestamp = None
    smallest_diff = None
    to_drop = False
    for timestamp in timestamps:
        time_diff = abs(target - timestamp)
        if smallest_diff is None or time_diff < smallest_diff:
            closest_timestamp = timestamp
            smallest_diff = time_diff

    if smallest_diff.total_seconds() > time_threshold:
        # print(f"Time difference too large for {target}.")
        closest_timestamp = None
        to_drop = True
        # print(f"{target} not good with {smallest_diff.total_seconds()}!")
        return closest_timestamp, to_drop

    # print(f"{target} good with {smallest_diff.total_seconds()}!")
    return closest_timestamp, to_drop
