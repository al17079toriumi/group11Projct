#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import logging


# レポート管理部
from c03.c06.write_feedback import write_feedback


app = Flask(__name__)


# フィードバックの書き込みをレポート管理部に依頼する関数
@app.route('/', methods=['GET', 'POST'])
def order_store_feedback():

    # user_idが見つからなかったらエラーを返す
    if 'user_id' not in request.form:
        logging.error("order_store_feedback: user_idをフォームから読み込めませんでした。")

    # assignment_idが見つからなかったらエラーを返す
    if 'assignment_id' not in request.form:
        logging.error("order_store_feedback: assignment_idをフォームから読み込めませんでした。")

    # assignment_idが見つからなかったらエラーを返す
    if 'feedback_text' not in request.form:
        logging.error("order_store_feedback: feedback_textをフォームから読み込めませんでした。")

    # フォームから受け取ったIDを格納
    user_id = request.form['user_id']

    # フォームから受け取った課題情報を格納
    assignment_id = request.form['assignment_id']

    # フォームから受け取ったフィードバックの内容を格納
    feedback_text = request.form['feedback_text']

    # レポート管理部へID、課題情報、フィードバックを渡して論理値を得る
    success = write_feedback(user_id, assignment_id, feedback_text)

    # 論理値の文字列を返す
    return str(success)


if __name__ == "__main__":
    app.run(debug=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s'
    )
