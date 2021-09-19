from pymon import posts, fill_data, login_db_check, users
import json
from bson import json_util
from uuid import uuid4 as uuid


def parse_json(data):
    return json.loads(json_util.dumps(data))


# sender = sender uuid
# send_amount = amount that need to send
# receiver = receiver uuid
# receiver_amount = amount that need to recive
# data = {
#                 'sender': input_json['sender'],
#                 'send_amount': input_json['send_amount'],
#                 'receiver': input_json['receiver']
#     }
def payment(input_json):
    data = {
                'sender': input_json['sender'],
                'send_amount': input_json['send_amount'],
                'receiver': input_json['receiver'],
                # 'receive_amount': input_json['receive_amount']
    }

    find_bal_receiver = users.find_one({'uid': data['receiver']})
    find_bal_sender = users.find_one({'uid': data['sender']})
    bal_receiver = int(find_bal_receiver['balance'])
    bal_sender = int(find_bal_sender['balance'])
    amount_to_send = str(bal_receiver + int(data['send_amount']))
    amount_to_deduct = str(bal_sender - int(data['send_amount']))

    
    try:
        #update the db with new value ---> completeting transaction
        users.update_one({'uid':data['sender']}, {'$set': {'balance': amount_to_deduct}})
        users.update_one({'uid':data['receiver']}, {'$set': {'balance': amount_to_send}})

        return {
                    'messge':'success',
                    'sender': amount_to_send,
                    'receiver': amount_to_deduct
        }
    except:
        return {'message': 'error'}
    pass


