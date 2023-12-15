import pandas as pd
import numpy as np
from toolkit import *
import config


def feature_20_27(date):

    '''
    :param date:
    :return: 共 8 个特征，每半小时成交量占总成交量的比例
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')

    file = file[['volume', 'code', 'time']]
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file.set_index(['code'], inplace = True)

    Time_Sheet = ["09:30:00", "10:00:00", "10:30:00", "11:00:00",
                  "11:30:00", "13:30:00", "14:00:00", "14:30:00", "15:00:00"]

    Time_Sheet = pd.to_datetime(Time_Sheet)
    Time_Sheet = [i.time() for i in Time_Sheet]

    ret = pd.DataFrame()
    ret['code'] = np.unique(file.index.tolist())
    ret['total_vol'] = file.groupby('code')['volume'].sum().values

    for i in range(0, len(Time_Sheet) - 1):
        L, R = Time_Sheet[i], Time_Sheet[i + 1]
        temp_df = file[file['time'].apply(lambda x: x.time() > L and x.time() <= R)]
        temp_df = temp_df.groupby('code')['volume'].sum()
        ret['feature_{}'.format(i + 20)] = temp_df.values / ret['total_vol']

    ret.drop('total_vol', axis = 1, inplace = True)
    ret = ret.reset_index(drop = True)
    # print(ret)
    # save_file(ret, 'feature_20_27', date, config.raw_save_path + 'feature_20_27', '.pkl'
    ret.to_pickle(r"{}/{}/{}/{}/{}.pkl".format(config.raw_save_path, "feature_20_27", date.year, date.month, date.strftime("%Y-%m-%d")))

def feature_28(date):
    '''
    :param date:
    :return:  方差比率，衡量成交量 5分钟和 10分钟的相关性
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'code', 'time']]

    file['volume_5'] = file.groupby('code')['volume'].rolling(5).sum().values
    file['volume_10'] = file.groupby('code')['volume'].rolling(10).sum().values

    var_1 = file.groupby('code')['volume_5'].var() / 5
    var_2 = file.groupby('code')['volume_10'].var() / 10
    code = var_1.index.tolist()

    ret = pd.DataFrame()
    ret['code'] = code
    ret['feature_28'] = (var_1 / var_2).values

    ret = ret.reset_index(drop=True)
    save_file(ret, 'feature_28', date, config.raw_save_path + 'feature_28', '.pkl')

def feature_29(date):
    '''
    :param date:
    :return: 前 30 min 和 午间休市后开盘 30 min 交易量比值
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'code', 'time']]

    LMT_1 = pd.to_datetime("10:00:00").time()

    df1 = file[file['time'].apply(lambda x: x.time() < LMT_1)]
    vol1 = df1.groupby('code')['volume'].sum()

    LMT_2 = pd.to_datetime("11:30:00").time()
    LMT_3 = pd.to_datetime("13:30:00").time()

    df2 = file[file['time'].apply(lambda x: x.time() > LMT_2 and x.time() < LMT_3)]
    vol2 = df2.groupby('code')['volume'].sum()

    code = vol1.index.tolist()

    ret = pd.DataFrame()
    ret['code'] = code
    ret['feature_29'] = (vol1 / vol2).values

    ret = ret.reset_index(drop = True)
    save_file(ret, 'feature_29', date, config.raw_save_path + 'feature_29', '.pkl')

if __name__ == '__main__':
    # feature_29(pd.to_datetime("2023-10-24"))

    feature_20_27(pd.to_datetime("2018-01-02"))

