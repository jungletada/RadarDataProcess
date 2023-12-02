import shutil
import os
import pandas as pd
from scipy.interpolate import interp1d
from path_configs import filter_path
from utils_read import data_mkdir

var_names = {
    'k': 'ka_band',
    'w': 'w_band',
    'p': 'pressure',
    't': 'temperature',
    'h': 'relativeHumidity',
    'lwc': 'lwc'}


def linear_interpolate(df, new_heights):
    """Function to perform linear interpolation"""
    interpolated_data = {}
    for column in df.columns:
        if column == 'Height':
            interpolated_data[column] = new_heights
        else:
            f = interp1d(df['Height'], df[column], kind='linear', fill_value='extrapolate')
            interpolated_data[column] = f(new_heights)
    return pd.DataFrame(interpolated_data)


def interpolate_on_band(selected_date):
    data_lwc = pd.read_csv(f'{filter_path}lwc/{selected_date}_lwc.csv')
    data_ka_band = pd.read_csv(f'{filter_path}ka_band/{selected_date}_ka_band.csv')
    data_w_band = pd.read_csv(f'{filter_path}w_band/{selected_date}_w_band.csv')
    heights_lwc = data_lwc['Height'].to_numpy()

    interpolated_ka = linear_interpolate(data_ka_band, heights_lwc)
    interpolated_w = linear_interpolate(data_w_band, heights_lwc)
    interpolated_ka.to_csv(
        f'{filter_path}ka_band/{selected_date}_ka_band.csv', index=False)
    interpolated_w.to_csv(
        f'{filter_path}w_band/{selected_date}_w_band.csv', index=False)


def move_file(new_path='data-ft-0'):
    data_mkdir(new_path)

    def move_band_files(file_list):
        for file in file_list:
            if "itp" not in file:
                src = os.path.join(old_path, file)
                dst = os.path.join(new_path, file)
                shutil.move(src, dst)

    for keys in ["ka_band", "w_band"]:
        old_path = f"{filter_path}{keys}/"
        file_list = os.listdir(old_path)
        move_band_files(file_list)


if __name__ == '__main__':
    from path_configs import dates_selection

    for date_ in dates_selection:
        # interpolate_on_band(selected_date=date_)
        move_file(new_path='data-ft-0')
