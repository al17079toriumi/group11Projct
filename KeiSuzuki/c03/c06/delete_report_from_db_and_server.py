from .connect_report_db import connect_report_db,close_db
import mysql.connector
import os
import logging

search_report = (
    "SELECT reportFilePath FROM test_table "
    "WHERE userID = %s AND homeworkID = %s"
)

delete_report_from_db = (
    "DELETE FROM test_table "
    "WHERE userID=%s AND homeworkID=%s "
)


def delete_report_from_db_and_server(user_id, homework_id):

    # check connect db is success
    cnx = connect_report_db()
    if cnx is None:
        logging.error("failed search report")
        return False

    # search report file path from db
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(search_report, (user_id, homework_id))
        get_dict_from_cursor = cursor.fetchone()
        cursor.close()

    except mysql.connector.Error as err:
        logging.error("failed search file")
        logging.error(err)
        close_db(cursor, cnx)
        return False
    logging.info("search report file from db success")

    # check report is exist
    if get_dict_from_cursor is None:
        logging.error("there is no report (user_id:%s, homework_id:%s)" % (user_id, homework_id))
        close_db(cursor, cnx)
        return False

    if 'reportFilePath' not in get_dict_from_cursor:
        logging.error("failed delete report from db")
        logging.error("there is no report")
        close_db(cursor, cnx)
        return False

    report_file_path = get_dict_from_cursor['reportFilePath']
    logging.info("report file path:"+report_file_path)

    # delete report from db
    try:
        # interrupt auto commit
        cnx.autocommit = False
        cursor = cnx.cursor()
        cursor.execute(delete_report_from_db, (user_id, homework_id))
        cursor.close()
    except mysql.connector.Error as err:
        print("failed delete from report_db")
        print(err)

    # try delete report file from directory
    try:
        os.remove(report_file_path)
        print("deleting report file from directory is success")
    except OSError as err:
        print("failed delete report file")
        print(err)
        cnx.rollback()
        close_db(cursor, cnx)
        return False
    except Exception as err:
        print("not expected err occur")
        print(err)
        cnx.rollback()
        close_db(cursor, cnx)
        return False

    # if deleting report file from directory is successful commit db
    cnx.commit()
    print("commit delete record")

    close_db(cursor, cnx)
    logging.info("close cursor and cnx")

    return True
