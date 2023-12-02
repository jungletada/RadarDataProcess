import pandas as pd
from utils_read import data_mkdir, get_csv_names, select_csv_from_date
from path_configs import raw_data_path, filter_path, data_path_dict, \
    txt_dict, var_names


def get_separate_pth(pth_list):
    pressure_path, temperature_path, humidity_path = [], [], []
    for file in pth_list:
        if 'pressure' in file:
            pressure_path.append(file)
        elif 'temperature' in file:
            temperature_path.append(file)
        else:
            humidity_path.append(file)
    return pressure_path, temperature_path, humidity_path


def filter_time_height_to_csv(
        csv_paths,
        key='ka',
        var_name='ka_band',
        selected_date='20121022',
        min_h=600.0,
        max_h=10000.0):
    timestamp_file = raw_data_path + f'{selected_date}/{selected_date}_{key}_filter.txt'
    with open(timestamp_file, 'r') as f:
        filter_timestamps = f.readlines()
    raw_dfs = [pd.read_csv(csv) for csv in csv_paths]
    res_df = [raw_dfs[0]['Height']]

    for raw_df in raw_dfs:
        res_timestamps = []
        for timestamp in filter_timestamps:
            timestamp = timestamp.strip()
            if timestamp in raw_df.columns:
                res_timestamps.append(timestamp)
        res_df.append(raw_df[res_timestamps])

    combine_df = pd.concat(res_df, axis=1)
    filtered_df = combine_df[(combine_df['Height'] >= min_h) & (combine_df['Height'] <= max_h)]
    filtered_df.to_csv(filter_path + f'{var_name}/{selected_date}_{var_name}.csv', index=False)


if __name__ == '__main__':
    data_mkdir(filter_path)
    from path_configs import dates_selection
    selected_csv = dict()
    for date_ in dates_selection:
        for key, txt in txt_dict.items():
            temp_csv = get_csv_names(txt)
            selected_csv_names = select_csv_from_date(temp_csv, date_)
            selected_csv[key] = [data_path_dict[key] + name for name in selected_csv_names]
            print(f"{key} selected: {selected_csv[key]}")

            if key == 'pth':
                pth_path_dict = dict()
                pth_path_dict['p'], pth_path_dict['t'], pth_path_dict['h'] = get_separate_pth(selected_csv[key])
                for k, pth_path in pth_path_dict.items():
                    data_mkdir(f'{filter_path}/{var_names[k]}/')
                    filter_time_height_to_csv(
                        pth_path, key=key, var_name=var_names[k], selected_date=date_,
                        min_h=600.0, max_h=10000.0)

            else:
                data_mkdir(f'{filter_path}/{var_names[key]}/')
                filter_time_height_to_csv(
                    selected_csv[key], key=key, var_name=var_names[key], selected_date=date_,
                    min_h=600.0, max_h=10000.0)
