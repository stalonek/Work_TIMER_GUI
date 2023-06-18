import time
import sqlite3
import logging
import sys
from datetime import datetime

class DBManager:
    """ Class responsible for data base management DB name: LoggingDB.db """
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        """DB connection set up"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            return self.connection
        except sqlite3.Error as e:
            print(f"DB connection has failed due to: {e.args[0]}")
            return None

    def disconnect(self):
        """DB disconnection"""
        self.connection.close()

    def write_to_db(self, time, date_of_study,  study_topic):
        """DB update with values"""

        cursor = self.connection.cursor()
        try:
            cursor.execute(f"INSERT INTO Logs (Time,'Study topic','Date of study') VALUES (?,?,?)", (time, study_topic, date_of_study,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Something went wrong with DB update due to: {e.args[0]}")

    def fetch_all(self):
        """ DB select * from"""

        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM Logs")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"DB operation has failed due to: {e.args[0]}")
            return None