#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import logging


# レポート管理部
from c03.c06.delete_report_from_db_and_server import delete_report_from_db_and_server


app = Flask(__name__)


# レポートの削除依頼をレポート管理部に依頼する関数
@app.route('/', methods=['GET', 'POST'])
def order_delete_report():

    # user_idが見つからなかったらエラーを返す
    if 'user_id' not in request.form:
        logging.error("order_report_file: user_idをフォームから読み込めませんでした。")

    # assignment_idが見つからなかったらエラーを返す
    if 'assignment_id' not in request.form:
        logging.error("order_report_file: assignment_idをフォームから読み込めませんでした。")

    # フォームから受け取ったIDを格納
    user_id = request.form['user_id']

    # フォームから受け取った課題情報を格納
    assignment_id = request.form['assignment_id']

    # レポート管理部へID、課題情報を渡して論理値を得る
    success = delete_report_from_db_and_server(user_id, assignment_id)

    # 論理値の文字列を返す
    return str(success)


if __name__ == "__main__":
    app.run(debug=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s'
    )
