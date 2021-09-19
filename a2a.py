import requests
import json
import uuid

url = "https://fusion.preprod.zeta.in/api/v1/ifi/{{ifiID}}/transfers"   # ifi id goes here
def transfer_money(from_acc,to_acc,amount,):
    payload = json.dumps({
    "requestID": str(uuid.uuid4()),
    "amount": {
        "currency": "INR",
        "amount":amount
    },
    "transferCode": "ATLAS_P2M_AUTH",
    "debitAccountID": from_acc,   
    "creditAccountID": to_acc,    
    "transferTime": 1574741608000,
    "remarks": "Fund Account Holders account",
    "attributes": {}
    })
    headers = {
    'Content-Type': 'application/json',
    'X-Zeta-AuthToken': 'Auth Key'      # Auth key goes here
    }  

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    #print(data['status'])
    #print(type(data))
    return data['status']
#print(transfer(x,y,1))
    
    
def transfer_money_from_funding(to_acc,amount):
    #uuid.uuid4()
    payload = json.dumps({
    "requestID": str(uuid.uuid4()),
    "amount": {
        "currency": "INR",
        "amount":amount
    },
    "transferCode": "ATLAS_P2M_AUTH",
    "debitAccountID": 'funding account id ',  #funding account id    
    "creditAccountID": to_acc,    
    "transferTime": 1574741608000,
    "remarks": "Fund Account Holders account",
    "attributes": {}
    })
    headers = {
    'Content-Type': 'application/json',
    'X-Zeta-AuthToken': 'Auth Key'      # Auth key goes here 
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    #print(data['status'])
    #print(type(data))
    return data['status']

    
def transfer_money_to_funding(from_acc,amount):
    #uuid.uuid4()
    payload = json.dumps({
    "requestID": str(uuid.uuid4()),
    "amount": {
        "currency": "INR",
        "amount":amount
    },
    "transferCode": "ATLAS_P2M_AUTH",
    "debitAccountID": from_acc,   
    "creditAccountID":'buffer_acc_no',    # Buffer account number
    "transferTime": 1574741608000,
    "remarks": "Fund Account Holders account",
    "attributes": {}
    })
    headers = {
    'Content-Type': 'application/json',
    'X-Zeta-AuthToken': 'Auth Key'      # Auth key goes here
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    #print(data['status'])
    #print(type(data))
    return data['status']

