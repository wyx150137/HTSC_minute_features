import pandas as pd
import numpy as np
from toolkit import load_file, save_file
import config

def feature_1(date) -> None:
    '''
    :param date:
    :return: 日内收益率
    '''
    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['open', 'close', 'code', 'time']]
    file.set_index(['code'], inplace = True)

    Begin_time = pd.to_datetime('09:31:00').time()
    End_time = pd.to_datetime('15:00:00').time()

    Open = file[file['time'].apply(lambda x: x.time()) == Begin_time]['open']
    Close = file[file['time'].apply(lambda x: x.time()) == End_time]['close']

    # return Close / Open - 1

    save_file(Close / Open - 1, 'feature_1', date, config.raw_save_path + 'feature_1', '.pkl')


def feature_2(date) -> None:
    '''
    :param date:
    :return: 收益率的方差
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['close', 'pre_close', 'code']]
    file.set_index(['code'], inplace = True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    ret = file.groupby('code')['ret'].std()

    save_file(ret, 'feature_2', date, config.raw_save_path + 'feature_2', '.pkl')

def feature_3(date) -> None:
    '''
    :param date:
    :return: 收益率的偏度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'close', 'pre_close']]

    file.set_index(['code'], inplace = True)
    file['ret'] = file['close'] / file['pre_close'] - 1

    ret = file.groupby('code')['ret'].apply(lambda x: x.skew())

    save_file(ret, 'feature_3', date, config.raw_save_path + 'feature_3', '.pkl')



def feature_4(date) -> None:
    '''
    :param date:
    :return: 收益率的峰度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'close', 'pre_close']]

    file.set_index(['code'], inplace = True)
    file['ret'] = file['close'] / file['pre_close'] - 1

    ret = file.groupby('code')['ret'].apply(lambda x: x.kurt())
    save_file(ret, 'feature_4', date, config.raw_save_path + 'feature_4', '.pkl')



def feature_5(date) -> None:
    '''
    :param date:
    :return: 典型价格差值
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'close', 'high', 'low', 'time']]
    file.set_index(['code'], inplace = True)

    Begin_time = pd.to_datetime('09:31:00').time()
    End_time = pd.to_datetime('15:00:00').time()

    df_open = file[file['time'].apply(lambda x: x.time()) == Begin_time]
    df_close = file[file['time'].apply(lambda x: x.time()) == End_time]

    A = (df_open['high'] + df_open['low'] + df_open['close']) / 3
    B = (df_close['high'] + df_close['low'] + df_close['close']) / 3

    ret = B - A

    save_file(ret, 'feature_5', date, config.raw_save_path + 'feature_5', '.pkl')



def feature_6(date) -> None:
    '''
    :param date:
    :return: 股价变动趋势占比
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file.set_index(['code'], inplace = True)

    Begin_time = pd.to_datetime('09:31:00').time()
    End_time = pd.to_datetime('15:00:00').time()

    Open = file[file['time'].apply(lambda x: x.time()) == Begin_time]['close']
    Close = file[file['time'].apply(lambda x: x.time()) == End_time]['close']

    up = Close - Open

    file['close_change'] = file['close'] - file['pre_close']
    file['close_change'] = np.abs(file['close_change'])
    file = file[file['time'].apply(lambda x: x.time()) != Begin_time]

    down = file.groupby('code')['close_change'].sum()

    ret = up / down
    save_file(ret, 'feature_6', date, config.raw_save_path + 'feature_6', '.pkl')



def feature_7(date) -> None:
    '''
    :param date:
    :return: 日内最大回撤
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'close', 'time']]
    file.set_index(['code'], inplace = True)

    file['max_close'] = file.groupby('code')['close'].cummax()
    file['drawdown'] = file['max_close'] / file['close']

    max_drawdown = file.groupby('code')['drawdown'].max() - 1

    ret = max_drawdown

    save_file(ret, 'feature_7', date, config.raw_save_path + 'feature_7', '.pkl')


def feature_8(date) -> None:
    '''
    :param date:
    :return: 日内最高价格出现时间 (如有多次，取第一次)
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'high', 'time']]
    file.set_index(['code'], inplace = True)

    file['max_high'] = file.groupby('code')['high'].max()
    file = file[file['high'] == file['max_high']]
    file['time'] = file['time'].apply(lambda x: x.time())
    Max_time = file.groupby('code')['time'].min()
    ret = Max_time

    save_file(ret, 'feature_8', date, config.raw_save_path + 'feature_8', '.pkl')

def feature_9(date) -> None:
    '''
    :param date:
    :return: 改进后日内涨幅
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['open', 'close', 'code', 'time']]
    file.set_index(['code'], inplace = True)

    Begin_time = pd.to_datetime('10:00:00').time()
    End_time = pd.to_datetime('15:00:00').time()

    Open = file[file['time'].apply(lambda x: x.time()) == Begin_time]['close']
    Close = file[file['time'].apply(lambda x: x.time()) == End_time]['close']

    ret = Close / Open

    save_file(ret, 'feature_9', date, config.raw_save_path + 'feature_9', '.pkl')



if __name__ == '__main__':
    feature_1(pd.to_datetime('2019-01-02'))