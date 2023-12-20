from jqdatasdk import *
import pandas as pd
import config
from .extract_files import extract_files

def login():
    auth(config.joint_quant_config['name'], config.joint_quant_config['password'])
    print(get_query_count())

def load_all_features(trade_cal, save_path):

    import os
    L = os.listdir(config.raw_save_path)

    all_features = L

    total_df = pd.DataFrame(columns=['code', 'time'])

    for item in all_features:
        print(item)
        df = extract_files(trade_cal, target_path = os.path.join(config.raw_save_path, item), file_format = '.pkl')
        df['time'] = pd.to_datetime(df['time'])
        total_df = pd.merge(total_df, df, on = ['code', 'time'], how = 'outer')
        print(total_df)
    total_df.to_pickle(save_path)


if __name__ == '__main__':
    load_all_features(None)