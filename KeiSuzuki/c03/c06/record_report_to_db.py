import mysql.connector
import logging

from .create_report_id import create_report_id
from .connect_report_db import connect_report_db, close_db


add_report_to_db = (
    "INSERT INTO test_table "
    "(userID, homeworkID, reportID, reportFilePath, feedBack)"
    "VALUES (%s, %s, %s, %s, %s)"
)

update_report_db = (
    "UPDATE test_table "
    "SET reportID = %s, reportFilePath = %s, feedBack= %s "
    "WHERE userID = %s AND homeworkID = %s"
)

check_user_submit = (
    "SELECT * FROM test_table "
    "WHERE userID=%s AND homeworkID=%s"
)


def record_report_to_db(save_file_path, user_id, homework_id):

    # connect reportDB
    cnx = connect_report_db()
    # check connect is success
    if cnx is None:
        logging.error("failed get connector")
        return False

    # interrupt auto commit
    cnx.autocommit = False

    report_id = create_report_id()
    if report_id == -1:
        logging.error("failed get new report_id")
        return False

    try:
        cursor = cnx.cursor()

        # check did user submit
        cursor.execute(check_user_submit, (user_id, homework_id))
        # did not submit
        if cursor.fetchone() is None:
            logging.info("user did not submitted")
            logging.info("insert to report_db")
            cursor.execute(add_report_to_db, (user_id, homework_id, report_id, save_file_path, ""))

        # did submit
        else:
            logging.info("user did submitted")
            logging.info("update report_db")
            cursor.execute(update_report_db, (report_id, save_file_path, "", user_id, homework_id))

    except mysql.connector.Error as err:
        logging.error("failed add report to db")
        logging.error(err)
        close_db(cursor, cnx)
        return False

    cnx.commit()

    cursor.close()
    cnx.close()

    logging.info("close connector")
    logging.info("insert report info success")

    return True
