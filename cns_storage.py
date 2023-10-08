import logging
import json
import time
import pandas as pd
from cns_common_functions import init_db_engine
from sqlalchemy import text


class jokes_storage:
    """
    Class to store jokes data in a database or file system
    """

    def __init__(self, config: dict):
        self.database = config['DATABASE']
        self.table = config['TABLE']
        self.engine = init_db_engine(config)
        self.connection = self.engine.connect()
        self.valid_storage = config["valid_storage"]
        self.invalid_storage = config["invalid_storage"]

        try:
            query = text(
                "IF NOT EXISTS (SELECT 1 FROM sys.databases where name = '" + self.database + "') CREATE DATABASE [" + self.database + "]")
            self.connection.execute(query)

        except Exception as e:
            logging.error("Error while checking if db exist: {}".format(e))
            raise

        try:
            query = text(
                "USE ["+self.database+"]; IF NOT EXISTS (SELECT 1 FROM sys.tables where name = '" + self.table + "') CREATE TABLE ["+self.database+"].[dbo].[" + self.table + "] ([id] [nvarchar](4000) NULL, [asdre] [bigint] NULL)")
            self.connection.execute(query)

        except Exception as e:
            logging.error("Error while crating table: {}".format(e))
            raise

    def __del__(self):
        self.connection.close()
        self.engine.dispose()

    @staticmethod
    def store_valid_data(data: dict, config: dict) -> bool:
        """
        Function to store data
        :param data: data to store
        :param config: config
        :return: True if success, False otherwise
        """
        try:
            # print(data)
            engine = init_db_engine(config)
            time_idx = str(time.time())
            with open(f"data_{time_idx}.json", "w") as f:
                json.dump(data, f)

        except Exception as e:
            logging.error("Error while storing data: {}".format(e))
            raise

        return True
