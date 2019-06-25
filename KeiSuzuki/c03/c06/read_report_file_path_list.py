import mysql.connector
from .connect_report_db import connect_report_db, close_db
import logging

read_user_submitted_report_list = (
    "SELECT reportFilePath FROM test_table "
    "WHERE userID=%s"
)


def read_report_file_path_list(user_id):

    cnx = connect_report_db()
    if cnx is None:
        logging.error("failed get connector")
        return list()

    try:
        cursor = cnx.cursor()
        cursor.execute(read_user_submitted_report_list, (user_id, ))
        result = cursor.fetchall()
        logging.info("get report list from db is success")

        cursor.close()
        cnx.close()
        logging.info("close connector")
    except mysql.connector.Error as err:
        logging.error("failed read report list from db")
        logging.error(err)
        close_db(cursor, cnx)
        return None

    # get only file name
    '''
    for i in range(0, len(result)):
        result[i] = result[i][0].split('\\').pop()
    '''
    # format to normal list
    for i in range(len(result)):
        temp = result[i][0]
        result[i] = temp

    logging.info("searching report list from db is success")
    close_db(cursor, cnx)
    logging.info("close cursor and cnx")
    return result
