import mysql.connector
from mysql.connector import errorcode

import logging

# I did this command
# mysql> GRANT ALL PRIVILEGES ON apply_1b.report_db TO 'SampUserName'@'localhost';
config = {
    'user': 'report_db_user',
    'password': 'qazwsx',
    'host': 'localhost',
    'database': 'report_db',
    'raise_on_warnings': True,
    'charset': 'utf8'
}


def connect_report_db():
    try:
        cnx = mysql.connector.connect(**config)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
        else:
            logging.error(err)

        return None
    else:
        logging.info("connect db")
        return cnx


def close_db(cursor, cnx):
    cursor.close()
    cnx.close()
