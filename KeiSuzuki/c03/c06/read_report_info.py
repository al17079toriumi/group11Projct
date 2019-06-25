from .connect_report_db import connect_report_db

import mysql.connector

import logging

search_users_reports = (
    "SELECT * FROM test_table "
    "WHERE userID = %s"
)


def read_report_info(user_id):

    cnx = connect_report_db()
    if cnx is None:
        logging.error("failed getting connector")
        return None

    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(search_users_reports, (user_id, ))
        users_report_info = cursor.fetchall()
        logging.info("reading report info from db is success")
    except mysql.connector.Error as err:
        logging.error("failed search users reports")
        logging.error(err)

    cursor.close()
    cnx.close()
    logging.info("close connector")

    # return list
    return users_report_info
