import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from concurrent.futures import ProcessPoolExecutor
from price_total import *
from price_part import *
from price_and_volume import *
from vol_or_money import *
from trading_and_price import *
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

def calc_vol_or_money_part(begin_date, end_date):
    trade_cal = get_trade_days(begin_date, end_date)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_20_27, trade_cal)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_28, trade_cal)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_29, trade_cal)


def calc_price_and_volume(begin_date, end_date):
    trade_cal = get_trade_days(begin_date, end_date)
    for num in range(36, 48):
        feature_name = 'feature_{}'.format(num)
        feature = eval(feature_name)
        print('now calculating {} ...'.format(feature_name))
        with ProcessPoolExecutor(max_workers = config.max_workers) as executor:
            executor.map(feature, trade_cal)
        print('done!')

def calc_trading_and_price(begin_date, end_date):
    trade_cal = get_trade_days(begin_date, end_date)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_30, trade_cal)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_31, trade_cal)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_32, trade_cal)
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_33_35, trade_cal)


if __name__ == '__main__':
    login()
    # calc_price_total_raw('2015-01-01', '2023-10-24')
    # calc_vol_or_money_part("2015-01-01", "2023-10-24")
    # calc_trading_and_price("2015-01-01", "2023-10-24")
    # calc_price_and_volume("2015-01-01", "2023-10-24")
    trade_cal = get_trade_days("2015-01-01", "2023-10-24")
    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        executor.map(feature_8, trade_cal)
