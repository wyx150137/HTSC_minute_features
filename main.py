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


if __name__ == '__main__':
    main()