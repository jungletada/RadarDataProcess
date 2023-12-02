from utils_read import get_timestamp_from_csv, \
    find_closest_timestamp, data_mkdir
from path_configs import raw_data_path
from utils_read import get_csv_names, select_csv_from_date


def separate_pth(pth_list):
    filter_path = []
    for file in pth_list:
        if 'pressure' in file:
            filter_path.append(file)
    return filter_path


def filter_time_stamp(date_select, txt_dict, data_path_dict):
    selected_csv = dict()
    for key, txt in txt_dict.items():
        temp_csv = get_csv_names(txt)
        selected_csv[key] = select_csv_from_date(temp_csv, date_select)

    # 选择同一日期的value的文件
    data_mkdir(raw_data_path + f"{date_select}")
    save_root = raw_data_path + f"{date_select}/"

    # 选择变量对应的csv文件
    selected_path_dict = dict()
    timestamps_dict = dict()
    for key, csv_list in selected_csv.items():
        selected_path_dict[key] = \
            [data_path_dict[key] + csv for csv in csv_list]
        if key == 'pth':
            temp_list = separate_pth(selected_path_dict['pth'])
            timestamps_dict['pth'] = get_timestamp_from_csv(temp_list)
        else:
            timestamps_dict[key] = get_timestamp_from_csv(selected_path_dict[key])

    # 挑选相近的时间戳
    # 对于{date}_ka中的每个时间戳，找到{date}_w中最接近的时间戳
    closest_time_dict = {'w': [], 'pth': [], 'lwc': []}
    ka_filter = timestamps_dict['ka'].copy()
    print(f"Original Ka-band length: {len(ka_filter)}")
    for index, target in enumerate(timestamps_dict['ka']):
        closest_in_w, w_for_drop = find_closest_timestamp(target, timestamps_dict['w'], time_threshold=120)
        closest_in_pth, pth_for_drop = find_closest_timestamp(target, timestamps_dict['pth'], time_threshold=120)
        closest_in_lwc, lwc_for_drop = find_closest_timestamp(target, timestamps_dict['lwc'], time_threshold=120)

        if w_for_drop or pth_for_drop or lwc_for_drop:
            ka_filter.remove(target)
            print(f"remove {target}")
        else:
            closest_time_dict['w'].append(closest_in_w)
            closest_time_dict['pth'].append(closest_in_pth)
            closest_time_dict['lwc'].append(closest_in_lwc)

    closest_time_dict['ka'] = ka_filter

    # 将结果写入到{date}_{val}_filter.txt
    def write_to_txt(time_lists, val):
        filter_file_path = save_root + f'{date_select}_{val}_filter.txt'
        with open(filter_file_path, 'w') as file:
            for ts in time_lists:
                file.write(ts.strftime('%Y/%m/%d %H:%M:%S') + '\n')

    for val in ['ka', 'w', 'pth', 'lwc']:
        write_to_txt(time_lists=closest_time_dict[val], val=val)


if __name__ == '__main__':
    from path_configs import dates_selection
    from path_configs import txt_dict, data_path_dict
    for date_ in dates_selection:
        filter_time_stamp(date_, txt_dict, data_path_dict)
