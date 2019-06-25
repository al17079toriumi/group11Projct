import mysql.connector
from .connect_report_db import connect_report_db, close_db
import logging

read_feedback_from_report_db = (
    "SELECT feedBack FROM test_table "
    "WHERE userID=%s AND homeworkID=%s "
    "LIMIT 1"
)


def read_feedback(user_id, homework_id):

    # connect to report_db
    cnx = connect_report_db()
    if cnx is None:
        logging.error("failed connect db")
        return ""

    result = ""

    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(read_feedback_from_report_db, (user_id, homework_id))
        dict_result = cursor.fetchone()

    except mysql.connector.Error as err:
        print("failed read feedback")
        print(err)
        result = ""

    # check record is exist
    if dict_result is None:
        logging.error("there is no record (user_id:%s, homework_id:%s)" % (user_id, homework_id))
        close_db(cursor, cnx)
        return ""

    if 'feedBack' not in dict_result:
        logging.error("dict does not have feedBack element")
        close_db(cursor, cnx)
        return ""

    feedback = dict_result['feedBack']
    logging.info("get feedback is successful")
    logging.info("feedback:"+feedback)

    cursor.close()
    cnx.close()
    logging.info("close connector")

    return feedback
