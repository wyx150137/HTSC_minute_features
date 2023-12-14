import pandas as pd
import numpy as np
from toolkit import *
import config

def feature_36(date):
    '''
    :param date:
    :return: VP 量价相关性
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'code', 'time']]

    VP = file.groupby('code').apply(lambda x: np.corrcoef(x['volume'], x['close'])[0, 1])
    ret = pd.DataFrame()
    code = VP.index.tolist()

    ret['code'] = code
    ret['feature_36'] = VP.values

    save_file(ret, 'feature_36', date, config.raw_save_path + 'feature_36', '.pkl')

def feature_37(date):
    '''
    :param date:
    :return:  VP_last_30_min 收盘前半小时的 VP
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'code', 'time']]

    LMT = pd.to_datetime("14:30:00").time()
    file = file[file['time'].apply(lambda x: x.time()) >= LMT].reset_index(drop = True)

    VP = file.groupby('code').apply(lambda x: np.corrcoef(x['volume'], x['close'])[0, 1])
    ret = pd.DataFrame()
    code = VP.index.tolist()

    ret['code'] = code
    ret['feature_37'] = VP.values

    save_file(ret, 'feature_37', date, config.raw_save_path + 'feature_37', '.pkl')

def feature_38(date):
    '''
    :param date:
    :return:  前 1/3 成交量对应的 VP
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'code', 'time']]

    file['volume_rank'] = file.groupby('code')['volume'].rank(ascending = False)
    file = file[file['volume_rank'] <= 80].reset_index(drop = True)

    VP = file.groupby('code').apply(lambda x: np.corrcoef(x['volume'], x['close'])[0, 1])
    ret = pd.DataFrame()
    code = VP.index.tolist()

    ret['code'] = code
    ret['feature_38'] = VP.values

    save_file(ret, 'feature_38', date, config.raw_save_path + 'feature_38', '.pkl')


def feature_39(date):
    '''
    :param date:
    :return: 收益率与成交量相关性 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]

    file['ret'] = file['close'] / file['pre_close'] - 1

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_39'] = VR.values

    save_file(ret, 'feature_39', date, config.raw_save_path + 'feature_39', '.pkl')

def feature_40(date):

    '''
    :param date:
    :return: 领先一分钟 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file = file.reset_index(drop = True)
    file['ret'] = file['close'] / file['pre_close'] - 1
    file['vol_1'] = file['volume'].shift(-1).values
    file.dropna(how = 'any', inplace = True)
    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['vol_1'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_40'] = VR.values

    save_file(ret, 'feature_40', date, config.raw_save_path + 'feature_40', '.pkl')

def feature_41(date):
    '''
    :param date:
    :return: 滞后一分钟 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file['ret'] = file['close'] / file['pre_close'] - 1
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file = file.reset_index(drop = True)
    file['vol_1'] = file.groupby('code')['volume'].shift(1).values
    file.dropna(how = 'any', inplace = True)
    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['vol_1'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_41'] = VR.values

    save_file(ret, 'feature_41', date, config.raw_save_path + 'feature_41', '.pkl')

def feature_42(date):
    '''
    :param date:
    :return: 收盘前半小时 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]

    LMT = pd.to_datetime("14:30:00").time()
    file = file[file['time'].apply(lambda x: x.time()) >= LMT].reset_index(drop = True)

    file['ret'] = file['close'] / file['pre_close'] - 1

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_42'] = VR.values

    save_file(ret, 'feature_42', date, config.raw_save_path + 'feature_42', '.pkl')

def feature_43(date):
    '''
    :param date:
    :return: 收盘前半小时领先 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file = file.reset_index(drop = True)
    file['volume_1'] = file.groupby('code')['volume'].shift(-1).values

    LMT = pd.to_datetime("14:30:00").time()
    file = file[file['time'].apply(lambda x: x.time()) >= LMT].reset_index(drop = True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file.dropna(how = 'any', inplace = True)

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume_1'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_43'] = VR.values

    save_file(ret, 'feature_43', date, config.raw_save_path + 'feature_43', '.pkl')


def feature_44(date):
    '''
    :param date:
    :return: 收盘前半小时领先 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file = file.reset_index(drop = True)
    file['volume_1'] = file.groupby('code')['volume'].shift(1)

    LMT = pd.to_datetime("14:30:00").time()
    file = file[file['time'].apply(lambda x: x.time()) >= LMT].reset_index(drop = True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file.dropna(how = 'any', inplace = True)

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume_1'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_44'] = VR.values

    save_file(ret, 'feature_44', date, config.raw_save_path + 'feature_44', '.pkl')

def feature_45(date):
    '''
    :param date:
    :return: 前 1/3 成交量 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file['volume_rank'] = file.groupby('code')['volume'].rank(ascending = False)
    file = file[file['volume_rank'] < 80].reset_index(drop = True)

    file['ret'] = file['close'] / file['pre_close'] - 1

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_45'] = VR.values

    save_file(ret, 'feature_45', date, config.raw_save_path + 'feature_45', '.pkl')


def feature_46(date):
    '''
    :param date:
    :return: 前 1/3 成交量领先 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file['volume_1'] = file.groupby('code')['volume'].shift(-1).values
    file['volume_rank'] = file.groupby('code')['volume'].rank(ascending = False)
    file = file[file['volume_rank'] < 80].reset_index(drop = True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file.dropna(how = 'any', inplace = True)

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume_1'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_46'] = VR.values

    save_file(ret, 'feature_46', date, config.raw_save_path + 'feature_46', '.pkl')

def feature_47(date):
    '''
    :param date:
    :return: 前 1/3 成交量滞后 VR
    '''

    file = load_file(date, config.my_file_path + 'minute_bar', '.pkl')
    file = file[['volume', 'close', 'pre_close', 'code', 'time']]
    file.sort_values(['code', 'time'], ascending = True, inplace = True)
    file = file.reset_index(drop = True)
    file['volume_1'] = file.groupby('code')['volume'].shift(1).values

    file['volume_rank'] = file.groupby('code')['volume'].rank(ascending = False)
    file = file[file['volume_rank'] < 80].reset_index(drop = True)

    file['ret'] = file['close'] / file['pre_close'] - 1
    file.dropna(how = 'any', inplace = True)

    VR = file.groupby('code').apply(lambda x: np.corrcoef(x['volume_1'], x['ret'])[0, 1])
    ret = pd.DataFrame()

    code = VR.index.tolist()
    ret['code'] = code
    ret['feature_47'] = VR.values
    print(ret)

    save_file(ret, 'feature_47', date, config.raw_save_path + 'feature_47', '.pkl')


if __name__ == '__main__':
    feature_38(pd.to_datetime("2023-12-04"))
    feature_39(pd.to_datetime("2023-12-04"))
    feature_40(pd.to_datetime("2023-12-04"))
    feature_41(pd.to_datetime("2023-12-04"))
    feature_42(pd.to_datetime("2023-12-04"))
    feature_43(pd.to_datetime("2023-12-04"))
    feature_44(pd.to_datetime("2023-12-04"))
    feature_45(pd.to_datetime("2023-12-04"))
    feature_46(pd.to_datetime("2023-12-04"))
    feature_47(pd.to_datetime("2023-12-04"))
