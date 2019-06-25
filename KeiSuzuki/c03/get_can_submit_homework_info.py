from flask import request, jsonify, Blueprint, render_template
import logging
import json

from c03.test_for_c03 import c9m2

get_can_submit_homework_info_app = Blueprint('get_can_submit_homework_info', __name__)
app = get_can_submit_homework_info_app


@app.route('/get_can_submit_homework_info', methods=['GET'])
def get_can_submit_homework_info():

    if request.method == 'GET':

        # get userID from request
        user_id = request.args.get('userID')
        if user_id is None:
            logging.error("userID not in prams")
            #return render_template("w7.html", "failed")
            return render_template("w7.html")
        else:
            logging.debug("request has userID")

        dict_of_homework_info = c9m2(user_id)
        if dict_of_homework_info is None:
            logging.error("failed get from c9m2")
            #return render_template("w7.html", "failed")
            return render_template("w7.html")
        else:
            logging.info("getting from c9m2 is success")

        logging.info("success get_can_submit_homework_info")

        str_json = json.dumps(dict_of_homework_info, ensure_ascii=False)

        #return render_template("w7.html", str_json)
        return render_template("w7.html")
