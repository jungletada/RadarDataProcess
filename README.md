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

### Attention! Below `py` file is to do post process on `data-ft`

- `post_process.py`: for ka-band and w-band, the moving average data is obtained, and results will be saved to `data-avg`
- `remove_duplicate.py` remove the duplicate data in LWC, and results will be saved to `data-slim`
  
    
