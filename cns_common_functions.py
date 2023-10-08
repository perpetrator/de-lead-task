import configparser
import logging


def load_config(config_file: str):
    """
    Function to load config file
    :param config_file: path to config file
    :return: config dictionary
    """
    try:
        print("Reading config file from: {}".format(config_file))
        config = configparser.ConfigParser()
        config.read(config_file)
    except Exception as e:
        print("Error while reading config file: {}".format(e))
        raise e
    return config
