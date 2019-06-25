#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify
import logging


# レポート管理部
from read_report_file_path import read_report_file_path
from c03.c06.read_feedback import read_feedback


app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False

# レポートとフィードバックを得る関数
@app.route('/', methods=['GET', 'POST'])
def order_report_file():

    # # user_idが見つからなかったらエラーを返す
    # if 'user_id' not in request.form:
    #     logging.error("order_report_file: user_idをフォームから読み込めませんでした。")
    #
    # # assignment_idが見つからなかったらエラーを返す
    # if 'assignment_id' not in request.form:
    #     logging.error("order_report_file: assignment_idをフォームから読み込めませんでした。")
    #
    # # フォームから受け取ったIDを格納
    # user_id = request.form['user_id']
    #
    # # フォームから受け取った課題情報を格納
    # assignment_id = request.form['assignment_id']

    # 上に四行をコメントアウトしてここを復活でTT可能
    # フォームから受け取ったIDを格納
    user_id = "1"

    # フォームから受け取った課題情報を格納
    assignment_id = "1"

    # レポート管理部へID、課題情報を渡してレポートファイルのパスを得る
    report_file_path = read_report_file_path(user_id, assignment_id)

    try:
        # レポートファイルを開く
        report_file = open(report_file_path, "r", encoding="UTF-8")
    except PermissionError:
        logging.error("order_report_file: パーミッションエラー")
    except IOError:
        logging.error("order_report_file: 入出力エラー")

    # レポートファイルを読み込む
    report_text_list = report_file.readlines()

    # レポートのテキストのリストを一つのテキストにする
    report_text = ""
    for line in report_text_list:
        report_text += line

    # レポート管理部へID、課題情報を渡してフィードバックのテキストを得る
    feedback_text = read_feedback(user_id, assignment_id)

    # 連想配列に追加
    result_dict = {
        "report_text": report_text,
        "feedback_text": feedback_text
    }
    # print(report_text)

    # jsonファイル風にする
    jsonify_result = jsonify(result_dict)

    # 返す
    return jsonify_result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="80")

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s'
    )
