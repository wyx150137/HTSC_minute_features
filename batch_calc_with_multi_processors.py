import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from concurrent.futures import ProcessPoolExecutor
from price_total import *
from price_part import *
from jqdatasdk import *
import config
import toolkit

def login():
    name = config.joint_quant_config['name']
    password = config.joint_quant_config['password']

    auth(name, password)
    print(get_query_count())

def calc_price_total_raw(begin_date, end_date):

    trade_cal = get_trade_days(begin_date, end_date)
    for num in range(1, 10):
        feature_name = 'feature_{}'.format(num)
        feature = eval(feature_name)
        print('now calculating {} ...'.format(feature_name))
        with ProcessPoolExecutor(max_workers = config.max_workers) as executor:
            executor.map(feature, trade_cal)
        print('done!')

def format_price(begin_date, end_date):
    trade_cal = get_trade_days(begin_date, end_date)
    for num in range(1, 10):
        feature_name = 'feature_{}'.format(num)
        print('now formatting {} ...'.format(feature_name))
        toolkit.format_files(trade_cal, config.raw_save_path, feature_name = feature_name, file_format = '.pkl')
        print('done!')

def calc_price_part_raw(begin_date, end_date):
    trade_cal = get_trade_days(begin_date, end_date)
    for num in range(10, 20):
        feature_name = 'feature_{}'.format(num)
        feature = eval(feature_name)
        print('now calculating {} ...'.format(feature_name))
        with ProcessPoolExecutor(max_workers = config.max_workers) as executor:
            executor.map(feature, trade_cal)
        print('done!')

if __name__ == '__main__':
    login()
    # calc_price_total_raw('2015-01-01', '2023-10-24')
    calc_price_part_raw("2015-01-01", "2023-10-24")


