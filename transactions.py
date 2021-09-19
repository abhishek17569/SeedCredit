import requests
import json
def transactions(accountID):
    url = "https://fusion.preprod.zeta.in/api/v1/ifi/{{ifiID}}/accounts/"+accountID+"/transactions?pageSize=50&pageNumber=1"   #ifiID here
    payload={}
    headers = {
    'X-Zeta-AuthToken': 'Auth Key'      # Auth key goes here
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    data=response.text
    data=json.loads(data)

