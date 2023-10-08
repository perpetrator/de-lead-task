import logging
import json

import pandas as pd
from cns_common_functions import init_db_engine
from sqlalchemy import text
from datetime import date


class jokes_storage:
    """
    Class to store jokes data in a database or file system
    """

    def __init__(self, config: dict):
        self.database = config['DATABASE']
        self.table = config['TABLE']
        self.engine = init_db_engine(config)
        self.connection = self.engine.connect()
        self.malformed_data_path = config['MALFORMED_DATA_PATH']

        try:
            query = text(
                "IF NOT EXISTS (SELECT 1 FROM sys.databases where name = '" + self.database + "') CREATE DATABASE [" + self.database + "]")
            self.connection.execute(query)
            self.connection.close()
            self.engine.dispose()
            logging.info("Database available")

            # after making sure that database exists, we can reinitialize engine
            self.engine = init_db_engine(config, database=self.database)
            self.connection = self.engine.connect()
            logging.debug("Database engine reinitialized")

        except Exception as e:
            logging.error("Error while checking if db exist: {}".format(e))
            raise

        try:
            query = text(
                "USE [" + self.database + "]; IF NOT EXISTS (SELECT 1 FROM sys.tables where name = '" + self.table + "') CREATE TABLE [" + self.database + "].[dbo].[" + self.table + "] ([categories] [nvarchar](4000) NULL, [created_at]  [nvarchar](4000) NULL, [icon_url] [nvarchar](4000) NULL, [id] [nvarchar](200) PRIMARY KEY CLUSTERED, [updated_at] [nvarchar](4000) NULL, [url] [nvarchar](4000) NULL, [value] [nvarchar](4000) NULL)")
            self.connection.execute(query)
            logging.info("Table " + self.table + " available")
        except Exception as e:
            logging.error("Error while crating table: {}".format(e))
            raise

    def __del__(self):
        self.connection.close()
        self.engine.dispose()

    def add_valid_data(self, data: pd.DataFrame):
        """
        Function to store data in a database
        :param data:
        """

        try:
            data.to_sql(
                "tmp_" + self.table,
                con=self.engine,
                index=False,
                if_exists="replace",
            )
            logging.info("Data stored in tmp table")

            query = "insert into " + self.table + "(" + """
                [categories]
                ,[created_at]
                ,[icon_url]
                ,[id]
                ,[updated_at]
                ,[url]
                ,[value])
                SELECT 
                [categories]
                ,[created_at] 
                ,[icon_url]
                ,[id]
                ,[updated_at]
                ,[url]
                ,[value]
                FROM """ + "tmp_" + self.table + " where id not in (select id from " + self.table + ")"

            self.connection.execute(text(query))
            logging.info("Data stored in main table")
            query = "drop table tmp_" + self.table
            self.connection.execute(text(query))
            logging.info("Temporary table dropped")

        except Exception as e:
            logging.error("Error while storing data: {}".format(e))
            raise

    @staticmethod
    def add_invalid_data(self, data):
        """
        Function to store malformed data in a file system
        :param self:
        :param data:
        """
        with open(f"{self.malformed_data_path}data_{str(date.today())}.json", "a") as f:
            json.dump(data, f)
        logging.info("Malformed data stored in: "+f"{self.malformed_data_path}data_{str(date.today())}.json")
