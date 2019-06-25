#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import logging


# レポート管理部
from c03.c06.read_report_list import read_report_list


app = Flask(__name__)


# レポートリストの読み込みをレポート管理部に依頼する関数
@app.route('/', methods=['GET', 'POST'])
def order_report_list():

    # user_idが見つからなかったらエラーを返す
    if 'user_id' not in request.form:
        logging.error("order_report_list: user_idをフォームから読み込めませんでした。")

    # フォームから受け取ったIDを格納
    user_id = request.form['user_id']

    # レポート管理部へIDを渡してレポートリストを得る
    report_list = read_report_list(user_id)

    # レポートのパスのリストを一つのテキストにする
    report_path_text = ""
    for line in report_list:
        report_path_text += (line + ",")

    # レポートのリストのテキストを返す
    return report_path_text


if __name__ == "__main__":
    app.run(debug=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s'
    )
