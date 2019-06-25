from .c06.delete_report_from_db_and_server import delete_report_from_db_and_server
from .c06.read_feedback import read_feedback
from .c06.write_feedback import write_feedback
from .c06.read_report_file_path_list import read_report_file_path_list

from flask import Flask, request, Blueprint, jsonify

test_for_c06_app = Blueprint('test_for_c06_app', __name__)
app = test_for_c06_app


@app.route('/delete_report_from_db_and_file', methods=['GET'])
def test_for_delete_report_from_db_and_file():
    user_id = request.args.get('userID')
    homework_id = request.args.get('homeworkID')

    result = delete_report_from_db_and_server(user_id, homework_id)
    print(result)

    return str(result)


@app.route('/read_feedback', methods=['GET'])
def test_for_read_feedback():
    user_id = request.args.get('userID')
    homework_id = request.args.get('homeworkID')

    result = read_feedback(user_id, homework_id)

    return str(result)


@app.route('/write_feedback', methods=['GET'])
def test_for_write_feedback():
    user_id = request.args.get('userID')
    homework_id = request.args.get('homeworkID')
    feedback = request.args.get('feedback')

    print(feedback)

    result = write_feedback(user_id, homework_id, feedback)
    print(result)

    #return str(result)

    str01 = "aAあああああああgafdaefa"

    samp01 =    {
        "ele01": str01
    }

    return jsonify(samp01)

@app.route('/read_report_list', methods=['GET'])
def test_for_read_report_file_path_list():
    user_id = request.args.get('userID')

    result = read_report_file_path_list(user_id)

    return str(result)


