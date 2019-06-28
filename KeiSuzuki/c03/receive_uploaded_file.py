from flask import Flask, request, jsonify, Blueprint, render_template, session
import logging
import os

from .save_uploaded_file import save_uploaded_file
from .c06.record_report_to_db import record_report_to_db


UPLOAD_FOLDER = 'up_folder'
ALLOWED_EXTENSIONS = set(['txt'])

receive_uploaded_file_app = Blueprint('receive_uploaded_file_app', __name__)
app = receive_uploaded_file_app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/receive_uploaded_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':

        # check need data is send
        if 'uploadedFile' not in request.files:
            logging.error("request don't have uploadedFile")
            return render_template("w9.html")

        if 'username' in session:
            user_id = session['username']
        else:
            logging.error("username not in session")

            #for debug
            user_id = "1"
            #return render_template("w9.html")

        if 'homeworkID' not in request.form:
            logging.error("request don't have homeworkID")
            return render_template("w9.html")

        # get data from post request
        homework_id = request.form['homeworkID']
        print("homeworkID"+homework_id)

        # check can int(str)
        try:
            print(user_id)
            print(homework_id)
            int(user_id)
            int(homework_id)
        except ValueError:
            logging.error("user_id or homework_id cannot format int")
            return render_template("w9.html")

        logging.info("getting userID and homeworkID is success")

        # check file is selected
        uploaded_file = request.files['uploadedFile']
        if uploaded_file.filename == '':
            logging.error("uploaded file is not selected")
            return render_template("w9.html")

        # check file has allowed extension
        if uploaded_file and allowed_file(uploaded_file.filename):
            logging.info("receive allowed extension file")
        else:
            logging.error("not allowed extension")
            return render_template("w9.html")

        # save uploaded file on server
        save_file_path = save_uploaded_file(user_id, homework_id, uploaded_file, UPLOAD_FOLDER)

        # if save file success insert to db
        if save_file_path == "":
            logging.error("failed save file")
            return render_template("w9.html")
        else:
            logging.info("saving file is success")

        # record report to db
        is_recording_report_success = record_report_to_db(save_file_path, user_id, homework_id)
        if is_recording_report_success:
            logging.info("record report to db is success")
        else:
            logging.error("record report to db is failed")
            try:
                os.remove(save_file_path)
            except OSError as err:
                logging.error("failed remove file " + save_file_path)
                logging.error(err)

            return render_template("w9.html")

    return render_template("w10.html")
