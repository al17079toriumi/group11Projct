from flask import request, jsonify, Blueprint, render_template, session
import logging
import json

from c03.test_for_c03 import c9m2

get_can_submit_homework_info_app = Blueprint('get_can_submit_homework_info', __name__, template_folder="templates")
app = get_can_submit_homework_info_app


@app.route('/get_can_submit_homework_info', methods=['GET'])
def get_can_submit_homework_info():

    if request.method == 'GET':

        if 'username' in session:
            user_id = session['username']
        else:
            user_id = "sample"

        homework_list = c9m2(user_id)
        if homework_list is None:
            logging.error("failed get from c9m2")
            return render_template("w7.html", error=True)
        else:
            logging.info("getting from c9m2 is success")

        logging.info("success get_can_submit_homework_info")

        return render_template("w7.html", homework_list=homework_list)
