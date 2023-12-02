# Radar-Data-Process
by Dingjie PENG, Waseda University

## Program description
### How to use  
1. Put all data (csv files) to `raw_data`, which should include 
    - ka-band: `\kasacrvpt`
    - w-band: `\wacr`
    - pressure, temperature, relativeHumidity: `\pth`
    - liquid water content:  `\lwc` 
2. run `main_process.py` to process all data, results are saved in `\data-ft`.

### File structure  

- `path_configs.py` : dates and dataset path  
- `walk_directory.py` : get all csv file names and convert timestamp format  
- `select_timestamp.py`: select the closest timestamps  
- `filter_csv.py`: select the appropriate  timestamps in CSV files according to `select_timestamp.py`  
- `interpolate_height.py`: filter out the height and do linear interpolation  

### 注意，以下py文件是在`data-ft`上做后处理
- `post_process.py` 对ka-band和w-band的数据求移动平均，然后保存到`data-avg`
- `remove_duplicate.py` 对LWC中的数据进行去重，结果保存到`data-slim`
  
    