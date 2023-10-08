import configparser
import logging
import pyodbc
from pandas import read_sql_query
from sqlalchemy import create_engine
from urllib import parse


def load_config(config_file: str) -> dict:
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


def init_db_engine(config) -> object:
    """
    Function initializes database engine using info from config and test it (by querying 'SELECT 1').

    :param config: Configuration of database
    :type config: dict
    :return: SQL Alchemy Engine
    :rtype: object
    """
    # odbc driver auto selection
    suitable_drivers = [
        driv for driv in pyodbc.drivers() if driv.endswith("SQL Server")
    ]
    drivers_ranking = [
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 14 for SQL Server",
        "ODBC Driver 13.1 for SQL Server",
        "ODBC Driver 13 for SQL Server",
        "ODBC Driver 11 for SQL Server",
        "SQL Server",
    ]
    driver = suitable_drivers[0]
    for driv in drivers_ranking:
        if driv in suitable_drivers:
            driver = driv
            break
    try:
        con_str = (
                "DRIVER="
                + driver
                + ";SERVER="
                + config["protocol"]
                + ":"
                + config["server"]
                + ";Port="
                + config["port"]
                + ";UID="
                + config["user"]
                + ";PWD="
                + config["password"]
        )
        quoted = parse.quote_plus(con_str)
        engine = create_engine(
            "mssql+pyodbc:///?odbc_connect={}".format(quoted),
            fast_executemany=True,
            connect_args = {'autocommit': True}
        )
        test_flag = read_sql_query("SELECT 1", engine)
        logging.info("DB connection established")
        return engine

    except Exception as e:
        logging.error(e)
        logging.critical("There were a problem with source DB connection!")
        # breaking without valid db connection
        raise
