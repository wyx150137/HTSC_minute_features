import pandas as pd
import numpy as np
from toolkit import load_file
import config

def alpha_1(date) -> pd.Series:
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

    return Close / Open - 1

def alpha_2(date) -> pd.Series:
    '''
    :param date:
    :return: 收益率的方差
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['close', 'pre_close', 'code']]
    file.set_index(['code'], inplace = True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    return file.groupby('code')['ret'].std()


def alpha_3(date) -> pd.Series:
    '''
    :param date:
    :return: 收益率的偏度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'close', 'pre_close']]

    file.set_index(['code'], inplace = True)
    file['ret'] = file['close'] / file['pre_close'] - 1

    return file.groupby('code')['ret'].apply(lambda x: x.skew())


def alpha_4(date) -> pd.Series:
    '''
    :param date:
    :return: 收益率的峰度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'close', 'pre_close']]

    file.set_index(['code'], inplace = True)
    file['ret'] = file['close'] / file['pre_close'] - 1

    return file.groupby('code')['ret'].apply(lambda x: x.kurt())


def alpha_5(date) -> pd.Series:
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

    return B - A



def alpha_6(date) -> pd.Series:
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

    return up / down


def alpha_7(date) -> pd.Series:
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

    return max_drawdown



if __name__ == '__main__':
    alpha_7(pd.to_datetime("2023-11-24"))