import pandas as pd
from path_configs import filter_path, dates_selection, var_names


def select_height(df, min_h=1000, max_h=8000):
    new_df = df[(df['Height'] >= min_h) & (df['Height'] <= max_h)]
    return new_df


def moving_average(df, window_size=30):
    new_df = pd.DataFrame(df['Height'])
    length = len(df.columns) - 1
    timestamps = df.columns[1:]

    for i in range(length - window_size + 1):
        window_columns = timestamps[i:i + window_size]
        avg_values = df[window_columns].mean(axis=1)
        avg_timestamp = pd.to_datetime(window_columns).mean()
        avg_timestamp_str = avg_timestamp.strftime('%Y/%m/%d %H:%M:%S')
        new_df[avg_timestamp_str] = avg_values

    return new_df


def delete_columns(df, window_size=30):
    new_df = pd.DataFrame(df['Height'])
    d = window_size // 2
    df_ = df.iloc[:, d: -d]
    new_df = pd.concat([new_df, df_], axis=1)
    return new_df

def rename_csv():
    import os
    save_path = 'data-ft'
    for date_ in dates_selection:
        for key in ["ka_band"]:
            old_file = f'{save_path}/{key}/{date_}_{key}_itp.csv'
            new_file = f'{save_path}/{key}/{date_}_{key}.csv'
            os.rename(old_file, new_file)


if __name__ == '__main__':
    # from utils_read import data_mkdir
    # save_path = 'data-avg/'
    # data_mkdir(save_path)
    # for var, varname in var_names.items():
    #     data_mkdir(f'{save_path}/{varname}')
    #     for date_ in dates_selection:
    #         if var == 'ka' or var == 'w':
    #             csv_file = f'{filter_path}/{varname}/{date_}_{varname}_itp.csv'
    #             print(f"Dealing with {csv_file}.")
    #             df = pd.read_csv(csv_file)
    #             new_df = select_height(df)
    #             new_df = moving_average(new_df)
    #             new_df.to_csv(f'{save_path}/{varname}/{date_}_{varname}.csv', index=False)
    #
    #         else:
    #             csv_file = f'{filter_path}/{varname}/{date_}_{varname}.csv'
    #             print(f"Dealing with {csv_file}.")
    #             df = pd.read_csv(csv_file)
    #             new_df = select_height(df)
    #             new_df = delete_columns(new_df)
    #             new_df.to_csv(f'{save_path}/{varname}/{date_}_{varname}.csv', index=False)
    rename_csv()
