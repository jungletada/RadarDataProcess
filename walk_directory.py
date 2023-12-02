import os
import pandas as pd
from dateutil import parser
from path_configs import txt_dict, data_path_dict


def walk_through(path_to_walk):
    file_names = []
    for root, dirs, files in os.walk(path_to_walk):
        for file in files:
            file_names.append(file)
    return file_names


def name_to_txt(filenames, txt_file):
    with open(txt_file, 'w') as f:
        for filename in filenames:
            f.write(filename + '\n')


def convert_date(time_string):
    try:
        dt = parser.parse(time_string, fuzzy=True)
        return dt.strftime('%Y/%m/%d %H:%M:%S')
    except ValueError:
        print(f"{time_string} not standard format")


def rename_column_all(csv_path):
    df = pd.read_csv(csv_path)
    new_col = ['Height'] + [convert_date(d) for d in df.columns[1:]]
    old_col = df.columns
    rename_dict = dict(zip(old_col, new_col))
    df.rename(columns=rename_dict, inplace=True)
    df.to_csv(csv_path, index=False)


def save_filenames_to_txt(txt_dict, data_path_dict):
    # 保存csv文件名到txt中
    for key, val_filepath in txt_dict.items():
        filenames = walk_through(data_path_dict[key])
        name_to_txt(filenames, txt_file=val_filepath)


def convert_time_format(txt_dict, data_path_dict):
    # 存储新的csv文件: 将所有时间戳转换为统一格式
    for key in data_path_dict.keys():
        with open(txt_dict[key], 'r') as f:
            for name in f.readlines():
                csv_path = data_path_dict[key] + name.strip()
                print(f"Converting time for {csv_path}")
                rename_column_all(csv_path)


if __name__ == '__main__':
    save_filenames_to_txt(txt_dict, data_path_dict)
    convert_time_format(txt_dict, data_path_dict)
