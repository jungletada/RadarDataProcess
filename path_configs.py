raw_data_path = 'raw_data/'
kacr_path = raw_data_path + 'kasacrvpt/'
wacr_path = raw_data_path + 'wacr/'
pth_path = raw_data_path + 'pth/'
lwc_path = raw_data_path + 'mwrp/'

ka_band_list = raw_data_path + 'ka-band.txt'
w_band_list = raw_data_path + 'w-band.txt'
pth_list = raw_data_path + 'pth.txt'
lwc_list = raw_data_path + 'lwc.txt'

filter_path = 'data-ft/'
data_path_dict = {
    'ka': kacr_path,
    'w': wacr_path,
    'pth': pth_path,
    'lwc': lwc_path
}

txt_dict = {
    'ka': ka_band_list,
    'w': w_band_list,
    'pth': pth_list,
    'lwc': lwc_list
}

var_names = {
    'ka': 'ka_band',
    'w': 'w_band',
    'p': 'pressure',
    't': 'temperature',
    'h': 'relativeHumidity',
    'lwc': 'lwc'}

dates_selection = [
    # "20121017",
    # "20121018",
    # "20121022",
    # "20121023",
    # "20121024",
    # "20121028",
    # "20121030",
    # "20121031",
    # "20121101",
    ## "20121102",
    ## "20121103",
    ## "20121104",
    ## "20121105",
    ## "20121106",
    ## "20121107",
    ## "20121113",
    ## "20121114",
    "20121115",
    # "20121117",
    # "20121121",
    # "20130214",
    # "20130215",
    # "20130218",
    # "20130405",
    # "20130406",
    # "20130407",
    # "20130514",
    # "20130515",
]
