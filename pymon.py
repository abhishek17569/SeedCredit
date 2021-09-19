#from app import transactions
from pymongo import MongoClient
import datetime
from pprint import pprint as pp

data = {
        "uid": "12_uuid",
        "user": {
            "name": 'demo name',
            # "adhar": input_json['adhar'],
            # "phone": input_json['phone'],
            # "email": input_json['email'],
            # "address": input_json['address'],
            # "pan": input_json['PAN'],
            # "bank_acc": input_json['Bank_Acc']
        },
        
        "timestamp": "12:12_timeStamp",
        "balance": "0",
        "extra": "Hell World",
        "video": "video_demo"
        }

client = MongoClient('127.0.0.1', 27017)
db = client.test_database
collection = db.test_collection

posts = db.posts
users = db.user
queues = db.queue
txn = db.transaction
loans= db.loan
# print(posts.find_one())
# user_id = users.insert_one(data).inserted_id
# print(user_id)
### fill data -> help in register and populate the data in mongoDB
def fill_data(reg_data):
    # post_id = posts.insert_one(post).inserted_id
    print(reg_data)
    print(users)
    users.insert_one(reg_data).inserted_id
    print("hello")
   

# print(posts)
# post_id = posts.insert_one(post).inserted_id
# post_id = posts.insert_one(post1).inserted_id

# print(db.list_collection_names())
# print(type(posts.find_one()))
# pp(posts.find_one())

#below check if user exist in db
def login_db_check(data):
    check = users.find_one({'user.email': data[0], 'user.password': data[1]})
    if check==None: return None
    else:
        return check

def login_db_check_uid(data):
    check = users.find_one({'uid': data})
    if check==None: return None
    else:
        return check

def find_all_queue(data):
    check = queues.find({'uid': data})
    if check==None: return None
    else:
        return check

def enqueue(data):
    queues.insert_one(data)
    return "inserted"

def add(data):
    txn.insert_one(data)
    return "trx complete" 

#### Get user detail by uid
def user_details(uid):
    user=users.find_one({'uid': uid})
    if user==None: return None
    else: return user

### loan past 
def loan_details(uid):
    data=users.find({'uid': uid})
    if data==None : return None
    else: return data

###update user balance loan and invest
def update_balance(uid,balance):
    data={"Balance":str(balance)}
    users.update_one({'uid':uid},{'$set':data})

def update_loan(uid,loan):
    data={"loan":str(loan)}
    users.update_one({'uid':uid},{'$set':data})

def update_invest(uid,invest):
    data={"invest":str(invest)}
    users.update_one({'uid':uid},{'$set':data})

#### get queue data

def fetch_active_queue(status):
    data=queues.find({'status' : str(status)})
    response_toList = []
    for res in data:
        print(res)
        # if res['status'] == 'active':
        #     valid_amount -= int(res['amount'])
        #     response_toList.append(parse_json(res))
    #print(response_toList)
    if data==None : return None
    else: return data
