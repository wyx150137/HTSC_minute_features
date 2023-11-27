import pandas as pd
import os
import datetime
def save_file(df, factor_name, time:datetime.datetime, path_name:str, file_format:str) -> None:
    '''
    :param path_name: path to store the file
    :param df: pd.DataFrame
    :param file_format: file format including '.'
    :return: None
    '''


    df = df.reset_index(drop = False)
    df.rename(columns = {'index': 'code'}, inplace = True)
    df.rename(columns = {0 : factor_name}, inplace = True)
    df['time'] = time

    path_name = path_name + '\\' + str(time.year) + '\\' + str(time.month)
    if not os.path.exists(path_name):
        os.makedirs(path_name)

    file_path = os.path.join(path_name, time.strftime("%Y-%m-%d") + file_format)

    if file_format == '.csv':
        df.to_csv(file_path)
    elif file_format == '.pkl':
        df.to_pickle(file_path)
    else:
        df.to_hdf(file_path, key = 'data', mode = 'w')

    return None