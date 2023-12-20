import pandas as pd
import numpy as np
from toolkit import *
import config


def feature_30(date):
    '''
    :param date:
    :return: WVAD 威廉变异离散量
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'time', 'open', 'high', 'volume', 'close', 'low']]

    file['WVAD'] = (file['close'] - file['open']) / (file['high'] - file['low']) * file['volume']
    WVAD = file.groupby('code')['WVAD'].sum()

    code = WVAD.index.tolist()
    ret = pd.DataFrame()
    ret['code'] = code
    ret['feature_30'] = WVAD.values

    print(ret)

    save_file(ret, 'feature_30', date, config.raw_save_path + 'feature_30', '.pkl')


def feature_31(date):
    '''
    :param date:
    :return: Amihud 收益率除以总交易金额
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'time', 'close', 'pre_close', 'volume']]

    file['ret'] = file['close'] / file['pre_close'] - 1
    file['Amihud'] = file['ret'] / file['volume'] / file['close']

    Amihud = file.groupby('code')['Amihud'].mean()

    code = Amihud.index.tolist()
    ret = pd.DataFrame()
    ret['code'] = code
    ret['feature_31'] = Amihud.values

    save_file(ret, 'feature_31', date, config.raw_save_path + 'feature_31', '.pkl')

def feature_32(date):
    '''
    :param date:
    :return: 正成交量指标，放量时收益率之和
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'time', 'close', 'pre_close', 'volume']]

    file['ret'] = file['close'] / file['pre_close'] - 1
    file['pre_volume'] = file.groupby('code')['volume'].shift(1)
    file['I'] = np.where(file['volume'] > file['pre_volume'], 1, 0)
    file['ret_I'] = file['ret'] * file['I']

    PVI = file.groupby('code')['ret_I'].sum()

    code = PVI.index.tolist()
    ret = pd.DataFrame()

    ret['code'] = code
    ret['feature_32'] = PVI.values

    save_file(ret, 'feature_32', date, config.raw_save_path + 'feature_32', '.pkl')

def feature_33_35(date):
    '''
    :param date:
    :return: 前 1/3 成交量对应的收益率方差，峰度，偏度
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['code', 'time', 'close', 'pre_close', 'volume']]
    file['ret'] = file['close'] / file['pre_close'] - 1

    file['vol_rank'] = file.groupby('code')['volume'].rank(ascending = False)
    file = file[file['vol_rank'] <= 80].reset_index(drop = True)

    var = file.groupby('code')['ret'].apply(lambda x: x.var())
    kurt = file.groupby('code')['ret'].apply(lambda x :x.kurt())
    skew = file.groupby('code')['ret'].apply(lambda x: x.skew())

    code = var.index.tolist()
    ret = pd.DataFrame()

    ret['code'] = code
    ret['feature_33'] = var.values
    ret['feature_34'] = kurt.values
    ret['feature_35'] = skew.values

    # save_file(ret, 'feature_33_35', date, config.raw_save_path + 'feature_33_35', '.pkl')
    ret.to_pickle(r"{}/{}/{}/{}/{}.pkl".format(config.raw_save_path, "feature_33_35", date.year, date.month, date.strftime("%Y-%m-%d")))

if __name__ == '__main__':
    feature_30(pd.to_datetime('2023-12-04'))
    # feature_33_35(pd.to_datetime('2023-12-04'))