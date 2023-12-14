import pandas as pd
import numpy as np
from toolkit import *
import config

def feature_10(date) -> None:
    '''
    :param date:
    :return: 收盘前半小时收益率
    '''
    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['open', 'close', 'code', 'time']]
    file.set_index(['code'], inplace = True)

    Begin_time = pd.to_datetime('14:31:00').time()
    End_time = pd.to_datetime('15:00:00').time()

    Open = file[file['time'].apply(lambda x: x.time()) == Begin_time]['close']
    Close = file[file['time'].apply(lambda x: x.time()) == End_time]['close']

    # return Close / Open - 1

    save_file(Close / Open, 'feature_10', date, config.raw_save_path + 'feature_10', '.pkl')


def feature_11(date) -> None:
    '''
    :param date:
    :return: 收盘前半小时的收益率方差
    '''


    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    Begin_time = pd.to_datetime('14:31:00').time()

    file['ret'] = file['close'] / file['pre_close'] - 1
    file = file[file['time'].apply(lambda x: x.time()) >= Begin_time]

    ret = file.groupby('code')['ret'].std()

    save_file(ret, 'feature_11', date, config.raw_save_path + 'feature_11', '.pkl')

def feature_12(date) -> None:
    '''
    :param date:
    :return: 收盘前半小时的收益率偏度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    Begin_time = pd.to_datetime('14:31:00').time()

    file['ret'] = file['close'] / file['pre_close'] - 1
    file = file[file['time'].apply(lambda x: x.time()) >= Begin_time]

    ret = file.groupby('code')['ret'].apply(lambda x: x.skew())

    save_file(ret, 'feature_12', date, config.raw_save_path + 'feature_12', '.pkl')

def feature_13(date) -> None:
    '''
    :param date:
    :return: 收盘前半小时的收益率峰度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    Begin_time = pd.to_datetime('14:31:00').time()

    file['ret'] = file['close'] / file['pre_close'] - 1
    file = file[file['time'].apply(lambda x: x.time()) >= Begin_time]

    ret = file.groupby('code')['ret'].apply(lambda x: x.kurt())

    save_file(ret, 'feature_13', date, config.raw_save_path + 'feature_13', '.pkl')

def feature_14(date) -> None:
    '''
    :param date:
    :return: 下行收益率方差
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file = file[file['ret'] < 0]
    ret = file.groupby('code')['ret'].std()
    ret.fillna(0, inplace = True)

    save_file(ret, 'feature_14', date, config.raw_save_path + 'feature_14', '.pkl')


def feature_15(date) -> None:
    '''
        :param date:
        :return: 上行收益率方差
        '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file = file[file['ret'] > 0]
    ret = file.groupby('code')['ret'].std()
    ret.fillna(0, inplace=True)

    save_file(ret, 'feature_15', date, config.raw_save_path + 'feature_15', '.pkl')

def feature_16(date) -> None:
    '''
    :param date:
    :return: 下行收益率方差占比
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    file['ret'] = file['close'] / file['pre_close'] - 1

    ret_total = file.groupby('code')['ret'].std()

    file = file[file['ret'] < 0]
    ret = file.groupby('code')['ret'].std()
    ret.fillna(0, inplace = True)

    ret = ret / ret_total

    save_file(ret, 'feature_16', date, config.raw_save_path + 'feature_16', '.pkl')

def feature_17(date) -> None:
    '''
    :param date:
    :return: 上行收益率方差占比
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    file['ret'] = file['close'] / file['pre_close'] - 1

    ret_total = file.groupby('code')['ret'].std()

    file = file[file['ret'] > 0]
    ret = file.groupby('code')['ret'].std()
    ret.fillna(0, inplace = True)

    ret = ret / ret_total

    save_file(ret, 'feature_17', date, config.raw_save_path + 'feature_17', '.pkl')


def feature_18(date) -> None:
    '''
    :param date:
    :return: 上行收益率波动占比 PS:这里研报里面应该是写反了
    由于 sqrt n 中的 n 是常数 240， 在标准化后不会影响因子，所以这里不进行计算了
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file['I'] = file['ret'] > 0
    file['ret_I'] = file['ret'] * file['I']
    file['ret_I'] = file['ret_I'].apply(lambda x: x**2)
    file['ret_2'] = file['ret'] ** 2

    ret_1 = file.groupby('code')['ret_I'].sum()
    ret_2 = file.groupby('code')['ret_2'].sum()

    ret = ret_1 / ret_2

    save_file(ret, 'feature_18', date, config.raw_save_path + 'feature_18', '.pkl')


def feature_19(date) -> None:
    '''
    :param date:
    :return: 前 10% 最大累计涨幅
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['pre_close', 'close', 'code', 'time']]
    file.set_index(['code'], inplace=True)

    file['ret'] = file['close'] / file['pre_close']
    file['ret_rank'] = file.groupby('code')['ret'].rank(ascending = False)
    file = file[file['ret_rank'] <= 10]

    ret = file.groupby('code')['ret'].prod()

    save_file(ret, 'feature_19', date, config.raw_save_path + 'feature_19', '.pkl')






if __name__ == '__main__':
    date = pd.to_datetime("2023-11-24")
    feature_19(date)


