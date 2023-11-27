import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from concurrent.futures import ProcessPoolExecutor
from price_and_money import *
from jqdatasdk import *
import config

def login():
    name = config.joint_quant_config['name']
    password = config.joint_quant_config['password']

    auth(name, password)
    print(get_query_count())

def calc_price_and_money_raw(begin_date, end_date):

    trade_cal = get_trade_days(begin_date, end_date)
    for num in range(1, 10):
        feature_name = 'feature_{}'.format(num)
        feature = eval(feature_name)
        print('now calculating {} ...'.format(feature_name))
        with ProcessPoolExecutor(max_workers = config.max_workers) as executor:
            executor.map(feature, trade_cal)
        print('done!')


if __name__ == '__main__':
    login()
    calc_price_and_money_raw('2015-01-01', '2023-10-24')



