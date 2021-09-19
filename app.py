from balance_check import balance
from flask import Flask, request, jsonify, render_template, make_response, redirect
from pymon import enqueue, posts, fill_data, login_db_check, find_all_queue , user_details ,loan_details,update_loan,update_balance,update_invest,fetch_active_queue
import json
from bson import json_util
from uuid import uuid4 as uuid
from pay import payment
# from timestamp import timestamp
from login import login, login_uid
from timestamp import timestamp_readable as timestamp
from new_acc import new_acc
from issue_bundle import issue
import uuid
from balance_check import balance , user_balance
from a2a import transfer_money,transfer_money_from_funding,transfer_money_to_funding

app = Flask(__name__,static_url_path="", static_folder="templates")

def parse_json(data):
    return json.loads(json_util.dumps(data))

#######################################################################################################################
 
@app.route('/')
def hello_world():
    # return 'This is my first API call!'
    return redirect('/register')

#########################################################################################################################

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True)
     print(input_json) 
     dictToReturn = {'text':input_json['text'],
                        'hell': input_json['hello']}
     return jsonify(dictToReturn)

#########################################################################################################################

@app.route('/getdata', methods=['GET'])
def getData():
    print(posts.find_one())
    data = posts.find_one()
    data_json= parse_json(data)
    return data_json

##############################################################################################################################
# Update route is used to update the data of the user.
@app.route('/update', methods=['POST'])
def register():
    input_json = request.get_json(force=True)
    print(input_json) 
    data = {
            "uid": "12_uuid",
            "user": {
                "name": input_json['name'],
                # "adhar": input_json['adhar'],
                # "phone": input_json['phone'],
                # "email": input_json['email'],
                # "address": input_json['address'],
                # "pan": input_json['PAN'],
                # "bank_acc": input_json['Bank_Acc']
            },
            
            "timestamp": str(timestamp),
            "balance": "0",
            "extra": "Hell World",
            "video": "demo_video"
            }
    try:
        fill_data(data)
        return jsonify({"message": "Successfully updated"})
    except:
        return jsonify({"message": "Error while updating the data"})
    pass


###############################################################################################################################
# /register route is used to register for the first time
@app.route('/register', methods = ['GET','POST'])
def first_time_register():
    # input_json = request.get_json(force=True)
    if request.method== 'POST':
        input_data = request.form
        pan="ABCD123456"
        phone=1234567890 
        uid = uuid.uuid4()
        # print(input_json)
        accountHolderID=new_acc(input_data['name'],input_data['phone'],input_data['pan'],str(uid))
        accountID=issue(accountHolderID,input_data['phone'])
        transfer_money_from_funding(accountID,500)
        print(accountHolderID)
        print(accountID)
        bal=balance(accountID)
        data = {
                    "uid": str(uid),
                    "user": {
                        "name": input_data['name'],
                        "email": input_data['email'],
                        "password": input_data['password'],
                        "PAN" : input_data['pan'],
                        "phone" : input_data['phone']

                    },
                    "timestamp": str(timestamp()),
                    "Balance": str(bal),
                    "accountHolderID" : accountHolderID, 
                    "accountID" : accountID,
                    "invest" : "0", 
                    "loan" : "0"
                }
        try:
            fill_data(data)
            res = parse_json({'message': 'Successfully registered. Please try login now.'})
            return make_response(render_template('login_reg.html', response=res))
        except:
            res = parse_json({'message': 'Error in registeration.'})
            return make_response(render_template('login_reg.html', response=res))
    else:
        if 'uid' in request.cookies:
            return make_response(redirect('/login'))
        res = parse_json({'message': ''})
        return make_response(render_template('login_reg.html', response=''))


##################################################################################################################################
# /login is used to login for already registerd user and return retrieved data
@app.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'GET':
        if 'uid' in request.cookies:
            cookie = str(request.cookies.get('uid'))
            print(cookie)
            check = login_uid(cookie)
            if check==None:
                return parse_json({'message': 'No user found'})
                # redirect_page = make_response(render_template('login_reg.html', response=response))
            else:
                response = parse_json(check)
                redirect_page = make_response(render_template('about.html', response=response))
                return redirect_page
        else:
            return render_template('index.html')
    if request.method == 'POST':

        if request.form['submit'] == 'Register For StartUp':
            # print("yes resigter starup")
            # response = parse_json({'message': 'Our Team will reach back to you!!'})
            redirect_page = make_response(render_template('startup_reg.html', response=''))
            return redirect_page

        email = request.form['email']
        password = request.form['password']
        # print(request.form)
        check = login(request.form)
        # print("here is error")
        # response = parse_json({'message': 'No user found'})
        if check==None:
            response =  parse_json({'message': 'No user found'})
            return make_response(render_template('login_reg.html', response=response))
        else:
            # return parse_json(check)
            # print(check)
            uid_cookie = check['uid']
            name_cookie = check['user']['name']
            response = parse_json(check)
            redirect_page = make_response(render_template('about.html', response=response))
            redirect_page.set_cookie('uid', str(uid_cookie), max_age=60*60*24*365*2)
            redirect_page.set_cookie('name', str(name_cookie), max_age=60*60*24*365*2)
            return redirect_page

        
    return render_template('index.html')

########################################################################################################################################
@app.route('/logout', methods=['POST'])
def logout():
    # res = parse_json({'message': ''})
    res = make_response(render_template('login_reg.html', response=''))
    res.set_cookie('uid', '',expires=0)
    return res

#########################################################################################################################################
@app.route('/transactions')
def transactions():
    name= 'null'
    uid = request.cookies.get('uid')
    name = request.cookies.get('name')
    # get data from transactions
    transaction_data='data'
    render_template('contact.html',transaction_data,name=name,uid=uid)


#########################################################################################################################################

@app.route('/invest',methods=['GET','POST'])
def invest():
    uid_user=request.cookies.get('uid')
    name_user=request.cookies.get('name')
    response=find_all_queue(uid_user)
    ball=user_balance(uid_user)
    #print(response[0]['status'])
    print((response))
    valid_amount=3000
    # for i in response:
    #     if response[i]['status'] == 'active':
    #         valid_amount-=response[i]['amount']
    response_toList = []
    for res in response:
        if res['status'] == 'active':
            valid_amount -= int(res['amount'])
            response_toList.append(parse_json(res))
            # print(res)
    if request.method == 'POST':
        amount=request.form['amount']
        if int(amount)>int(valid_amount):
            return render_template('invest.html',response=response_toList,valid_amount=valid_amount,out='Already in queue or try with available amount',ball=ball)
        else:
            time=timestamp()
            #status='active'
            data={
                "uid": uid_user,
                "order_no": "100",        
                "timestamp": time,
                "amount": amount,
                "status": "active",
            }
            print(data)
            enqueue(data)
            response=find_all_queue(uid_user)
            response_toList = []
            for res in response:
                if res['status'] == 'active':
                    valid_amount -= int(res['amount'])
                    response_toList.append(parse_json(res)) 
            ball=user_balance(uid_user)
            return make_response(render_template('invest.html',amount=amount,valid_amount=valid_amount,out="Added in Queue",response=response_toList,ball=ball))
    else:
        return make_response(render_template('invest.html',name=name_user,valid_amount=valid_amount,out="",response=response_toList,ball=ball))

#########################################################################################################################################

@app.route('/loan',methods=['GET','POST'])
def loan():
    uid_user=request.cookies.get('uid')
    name_user=request.cookies.get('name')
    user=user_details(uid_user)
    print(user['accountID'])
    loan_data=loan_details(uid_user)
    max_limit=2000
    past_loan=user['loan']
    valid_amount=max_limit-int(past_loan)
    valid_amount=int(valid_amount)
    ball=user_balance(uid_user)
    if request.method == 'POST':
        amount=request.form['amount']
        if int(amount) <= int(valid_amount):    
            transfer_money_from_funding(user['accountID'], amount)
            bal=balance(user['accountID'])
            update_loan(uid_user,str(int(amount)+int(past_loan)))
            update_balance(uid_user,bal) 
            valid_amount=str(int(valid_amount)-int(amount))
            ball=user_balance(uid_user)  
            loan=str(int(amount)+int(past_loan))   
            return make_response(render_template('loan.html',loan=loan,ball=ball,name=name_user,valid_amount=valid_amount,out1="Rs"+amount+" added to your account",out2="Your updated balance is Rs "+str(bal),response=loan_data))
        else:    
            return make_response(render_template('loan.html',loan=past_loan,ball=ball,name=name_user,valid_amount=valid_amount,out1="Limit 0 or select amount <= valid limit",out2="",response=loan_data))
        
    else:
        return make_response(render_template('loan.html',loan=past_loan,ball=ball,name=name_user,valid_amount=valid_amount,out1="",out2="",response=loan_data))

# @app.route('/payloan')
#     def(payloan)
#########################################################################################################################################    
## Payment api
@app.route('/payment', methods=['POST'])
def payment_api():
    message = payment(request.get_json(force=True))
    return parse_json(message)

#########################################################################################################################################

@app.route('/invest_detail', methods=['GET'])
def showInvestDetails():
    if request.method == 'GET':
        uid = request.cookies.get('uid')
        check = login_uid(uid)
        ball=user_balance(uid)
        # transaction = check['transaction']
        name = request.cookies.get('name')
        # return make_response(render_template('contact.html', response=transaction, name=name))
        return make_response(render_template('contact.html', response='', name=name,ball=ball))

############################################### Startup Investment #####################################################################

@app.route('/startup')
def startup():
    name = request.cookies.get('name')
    uid = request.cookies.get('uid')
    ball= user_balance(uid)
    return render_template('portfolio.html', name=name,ball=ball)
########################################################################################################################################

@app.route('/start123',methods=['GET','POST'])
def startuppage1():
    uid_user=request.cookies.get('uid')
    name_user=request.cookies.get('name')
    ball=user_balance(uid_user)
    user=user_details(uid_user)
    bal=user['Balance']
    startup_uid='startup_account_id' # startup account id goes here
    startup_data=user_details(startup_uid)
    target_funds=startup_data['invest']
    raised_funds=startup_data['loan']
    startup_accountID=startup_data['accountID']
    print(user['accountID'])
    if request.method == 'POST':
        amount=request.form['amount']
        if int(amount) <= int(bal):    
            transfer_money(user['accountID'],startup_accountID,amount)
            bal=balance(user['accountID'])
            update_balance(uid_user,bal) 
            raised_funds=str(int(raised_funds)+int(amount)) 
            update_loan(startup_uid,raised_funds)
            s_bal=str(int(startup_data['Balance']) + int(amount))
            update_balance(startup_uid,s_bal)
            ball=user_balance(uid_user)    
            return make_response(render_template('portfolio-details.html',ball=ball,out1="Rs"+amount+" invested in the startup",target_funds=target_funds,raised_funds=raised_funds,name=name_user))
        else:    
            return make_response(render_template('portfolio-details.html',ball=ball,out1="Low Balance",target_funds=target_funds,raised_funds=raised_funds,name=name_user))
        
    else:
        return make_response(render_template('portfolio-details.html',ball=ball,out1="",target_funds=target_funds,raised_funds=raised_funds,name=name_user))

############################################### TERMS ##################################################################################
@app.route('/start1234',methods=['GET','POST'])
def startuppage2():
    uid_user=request.cookies.get('uid')
    name_user=request.cookies.get('name')
    ball=user_balance(uid_user)
    user=user_details(uid_user)
    bal=user['Balance']
    startup_uid='startup_account_id' # startup account id goes here
    startup_data=user_details(startup_uid)
    target_funds=startup_data['invest']
    raised_funds=startup_data['loan']
    startup_accountID=startup_data['accountID']
    print(user['accountID'])
    if request.method == 'POST':
        amount=request.form['amount']
        if int(amount) <= int(bal):    
            transfer_money(user['accountID'],startup_accountID,amount)
            bal=balance(user['accountID'])
            update_balance(uid_user,bal) 
            raised_funds=str(int(raised_funds)+int(amount)) 
            update_loan(startup_uid,raised_funds)
            s_bal=str(int(startup_data['Balance']) + int(amount))
            update_balance(startup_uid,s_bal)
            ball=user_balance(uid_user)    
            return make_response(render_template('portfolio-details1.html',ball=ball,out1="Rs"+amount+" invested in the startup",target_funds=target_funds,raised_funds=raised_funds,name=name_user))
        else:    
            return make_response(render_template('portfolio-details1.html',ball=ball,out1="Low Balance",target_funds=target_funds,raised_funds=raised_funds,name=name_user))
        
    else:
        return make_response(render_template('portfolio-details1.html',ball=ball,out1="",target_funds=target_funds,raised_funds=raised_funds,name=name_user))

########################################################################################################################################
@app.route('/terms')
def terms():
    name = request.cookies.get('name')
    uid = request.cookies.get('uid')
    ball=user_balance(uid)
    return render_template('terms.html', name=name,ball=ball)

#######################################################################################################################################


@app.route('/startup_reg', methods=['POST'])
def startUp_reg():
    message = parse_json({'message': 'Thank you! Our team will call you!!'})
    return make_response(render_template('startup_reg.html', response=message))

#######################################################################################################################################

@app.route('/fillbuffer')
def fill():
    fundingAccountID='buffer_account_id' # buffer account id goes here
    data=''
    bal = balance(fundingAccountID)
    threshold=5000
    amount=0
    if(bal<threshold):
        data=fetch_active_queue('active')
        for res in data:
            print(res)
            if(amount<=2000):
                amount=amount+res['amount']
                user=user_details(res['uid'])
                email_id=user['user']['email']
                #payment_email(email_id,res['amount'],data)
                # transfer_money_to_funding(user['accountID'],res['amount'])
                print(res['amount'])

@app.route('/update_details', methods=['GET','POST'])
def register_12():
    if request.method == 'POST':
        # input_json = request.get_json(force=True)
        # try:
            # fill_data(data)
        res =  parse_json({"message": "Successfully updated"})
        return make_response(render_template('data_update.html', response=res))
        # except:
        #     return jsonify({"message": "Error while updating the data"})
        # pass
    else:
        # res =  parse_json({"message": ""})
        return make_response(render_template('data_update.html', response=''))


if __name__ == "__main__":
    app.run(debug=True)
    
    