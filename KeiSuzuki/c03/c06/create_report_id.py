from .connect_report_db import connect_report_db
import random
import mysql.connector
import logging

search_report_id_exist = (
    "SELECT * FROM test_table "
    "WHERE reportID=(%s)"
)


def create_report_id():

    cnx = connect_report_db()
    # check connecting to report_db is success
    if cnx is None:
        logging.error("failed get connector")
        return -1
    cursor = cnx.cursor()

    report_id = -1

    while True:
        report_id = random.randint(0, 100000)
        try:
            cursor.execute(search_report_id_exist, (int(report_id),))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            report_id = -1
            result = "failed sql"
            logging.error("search report id is failed")
            logging.error(err)

        if result is None:
            break
        else:
            logging.info(report_id+" is still used")

    logging.info("success create new reportID")

    cursor.close()
    cnx.close()
    logging.info("close connector")

    return report_id
