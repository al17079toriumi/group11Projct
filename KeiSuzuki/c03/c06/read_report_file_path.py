from .connect_report_db import connect_report_db, close_db
import mysql.connector
import logging

search_report_file_path = (
    "SELECT filePath FROM test_table "
    "WHERE userID = %s AND homeworkID = %s"
)


def read_report_file_path(user_id, homework_id):

    cnx = connect_report_db()
    if cnx is None:
        logging.error("failed getting connector")
        return None

    try:
        cursor = cnx.cursor()
        cursor.execute(search_report_file_path, (user_id, homework_id))
        report_file_path_list = cursor.fetchall()
        logging.info("read report file path list from db is success")
    except mysql.connector.Error as err:
        logging.error("failed search users reports")
        logging.error(err)

    close_db(cursor, cnx)
    logging.info("close connector")

    # return list
    return report_file_path_list[0]
