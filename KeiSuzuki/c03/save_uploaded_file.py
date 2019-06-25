import os
from werkzeug.utils import secure_filename
import logging


def save_uploaded_file(user_id, homework_id, uploaded_file, basic_dir):

    secured_filename = secure_filename(uploaded_file.filename)
    save_dir_path = os.path.join(basic_dir, user_id)
    save_dir_path = os.path.join(save_dir_path, homework_id)

    if os.path.exists(save_dir_path):
        is_dir_exist = True
    else:
        is_dir_exist = False

    if is_dir_exist:
        pass
    else:
        os.makedirs(save_dir_path)

    try:
        save_file_path = os.path.join(save_dir_path, secured_filename)
        uploaded_file.save(save_file_path)
    except Exception as err:
        logging.error("failed save")
        logging.error(err)
        save_file_path = ""

    return save_file_path
