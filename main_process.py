from walk_directory import save_filenames_to_txt, convert_time_format
from select_timestamp import filter_time_stamp
from filter_csv import get_csv_names, \
    get_separate_pth, filter_time_height_to_csv
from interpolate_height import interpolate_on_band, move_file
from path_configs import dates_selection, filter_path
from path_configs import txt_dict, data_path_dict, var_names
from utils_read import data_mkdir, select_csv_from_date


if __name__ == '__main__':
    save_filenames_to_txt(txt_dict, data_path_dict)
    convert_time_format(txt_dict, data_path_dict)

    data_mkdir(filter_path)
    selected_csv = dict()
    min_h, max_h = 600.0, 10000.0
    for date_ in dates_selection:
        filter_time_stamp(date_, txt_dict, data_path_dict)

        for key, txt in txt_dict.items():
            temp_csv = get_csv_names(txt)
            selected_csv_names = select_csv_from_date(temp_csv, date_)
            selected_csv[key] = [data_path_dict[key] + name for name in selected_csv_names]
            print(f"{key}: {selected_csv[key]}")

            if key == 'pth':
                pth_path_dict = dict()
                pth_path_dict['p'], pth_path_dict['t'], pth_path_dict['h'] = get_separate_pth(selected_csv[key])
                for k, pth_path in pth_path_dict.items():
                    data_mkdir(f'{filter_path}{var_names[k]}/')
                    filter_time_height_to_csv(
                        pth_path, key=key, var_name=var_names[k], selected_date=date_,
                        min_h=min_h, max_h=max_h)

            else:
                data_mkdir(f'{filter_path}{var_names[key]}/')
                filter_time_height_to_csv(
                    selected_csv[key], key=key, var_name=var_names[key], selected_date=date_,
                    min_h=min_h, max_h=max_h)

        interpolate_on_band(selected_date=date_)
        # move_file(new_path='data-ft-0')
