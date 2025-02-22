from flask import Flask

from c03.get_can_submit_homework_info import get_can_submit_homework_info_app
from c03.test_for_c06 import test_for_c06_app
from c03.receive_uploaded_file import receive_uploaded_file_app

# from c03.config import c03_module

import logging

app = Flask(__name__)
app.debug = True

app.register_blueprint(get_can_submit_homework_info_app)
app.register_blueprint(test_for_c06_app)
app.register_blueprint(receive_uploaded_file_app)

app.config['JSON_AS_ASCII'] = False

'''
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)
'''

logging.basicConfig(
    level=logging.DEBUG,
    format='%(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)

if __name__ == '__main__':
    logging.debug("run app")
    app.run(host='0.0.0.0', port=80)
