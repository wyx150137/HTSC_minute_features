import config
import toolkit
from toolkit import extract_files
from jqdatasdk import *

def login():
    name = config.joint_quant_config['name']
    password = config.joint_quant_config['password']

    auth(name, password)
    print(get_query_count())


def main():
    login()
    trade_cal = get_trade_days("2018-01-01", "2019-01-01")
    toolkit.load_all_features(trade_cal, "total_feature.pkl")


if __name__ == '__main__':
    main()