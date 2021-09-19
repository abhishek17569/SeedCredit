from pymon import posts, fill_data, login_db_check, users, login_db_check_uid
import json
from bson import json_util
from uuid import uuid4 as uuid
from pymon import login_db_check


def login(input_form):
    # input_json = request.get_json(force=True)
    # data = {
    #             'email': input_json['email'],
    #             'password': input_json['password']
    #         }
    # print((input_form['email']))
    data = [input_form['email'], str(input_form['password'])]
    check = login_db_check(data)
    return check

def login_uid(data):
    check = login_db_check_uid(data)
    return check
    