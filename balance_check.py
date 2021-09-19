import requests
import json
from pymon import user_details

def balance(acc):
    url = "https://fusion.preprod.zeta.in/api/v1/ifi/{{ifiID}}/accounts/" + acc+"/balance" # ifiID add here
    payload={}
    headers = {
    'X-Zeta-AuthToken': 'Auth Key'      # Auth key goes here
     }
    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    return data['balance']

def user_balance(uid):
    user_data=user_details(uid)
    acc=user_data['accountID']
    return balance(acc)


