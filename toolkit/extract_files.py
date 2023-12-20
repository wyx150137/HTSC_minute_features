import pandas as pd
import numpy as np
import datetime
import os


def extract_files(trade_cal: list[datetime.datetime], target_path: str, file_format: str, key_word = None) -> pd.DataFrame:
    '''
    :param trade_cal: list of datetime.datetime
    :param target_path: path to store the files
    :param file_format: file format including '.'
    :param key_word: key word for hdf5 file, if file_format is not hdf5, this parameter is not needed
    :return: pd.DataFrame
    '''

    if not os.path.exists(target_path):
        raise Exception('File path does not exist!')

    if file_format not in ['.csv', '.pkl', '.hdf', '.hdf5', '.h5']:
        raise Exception('File format is not supported!')


    df_L = []

    for date in trade_cal:
        year = date.year
        month = date.month

        file_path = os.path.join(target_path, str(year), str(month), date.strftime("%Y-%m-%d") + file_format)

        if file_format == '.csv':
            df = pd.read_csv(file_path)
        elif file_format == '.pkl':
            df = pd.read_pickle(file_path)
        else:
            df = pd.read_hdf(file_path, key = key_word)

        if "time" not in df.columns:
            df['time'] = date.strftime("%Y-%m-%d")

        df_L.append(df)

    ret_df = pd.concat(df_L).reset_index(drop = True)

    return ret_df

