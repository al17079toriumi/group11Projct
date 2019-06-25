from .connect_report_db import connect_report_db, close_db

import mysql.connector

import logging

write_feedback_to_report_db = (
    "UPDATE test_table "
    "SET feedBack=%s "
    "WHERE userID=%s AND homeworkID=%s "
)

search_record_is_exist = (
    "SELECT * FROM test_table "
    "WHERE userID=%s AND homeworkID=%s"
)


def write_feedback(user_id, homework_id, feedback):

    cnx = connect_report_db()
    if cnx is None:
        logging.error("failed get connector")
        return False

    # interrupt auto commit
    cnx.autocommit = False

    # search record is exist
    try:
        cursor = cnx.cursor()
        cursor.execute(search_record_is_exist, (user_id, homework_id))
        search_result = cursor.fetchone()
    except mysql.connector.Error as err:
        logging.error("failed search record")
        logging.error(err)
        close_db(cursor, cnx)
        return False

    # check record is exist
    if search_result is None:
        logging.error("there is no record (user_id,homework_id)=(%s,%s)" %(user_id,homework_id))
        close_db(cursor, cnx)
        return False
    else:
        logging.info("there is record (user_id,homework_id)=(%s,%s)" %(user_id,homework_id))

    try:
        cursor = cnx.cursor()
        cursor.execute(write_feedback_to_report_db, (feedback, user_id, homework_id))
        cnx.commit()
    except mysql.connector.Error as err:
        logging.error("failed write feedback to report_db")
        logging.error(err)
        close_db(cursor, cnx)
        return False

    cursor.close()
    cnx.close()
    logging.info("close connector")

    return True
