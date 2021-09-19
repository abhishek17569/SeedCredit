import requests
import json
#bundleid='a07f0c63-2709-4ba4-b93f-ac1531b9593f'
def issue(individual_id,p_no):

    url = "https://fusion.preprod.zeta.in/api/v1/ifi/{{ifiID}}/bundles/{{bundleID}}/issueBundle" #ifiID and bundleID here

    payload = json.dumps({
    "accountHolderID": individual_id,
    "disableCardFFCreation": False,
    "disableFFCreation": False,
    "disablePhoneFFCreation": False,
    "name": "Bundle 1",
    "phoneNumber": p_no
    })
    headers = {
    'Content-Type': 'application/json',
    'X-Zeta-AuthToken':'Auth Key'      # Auth key goes here
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    data=response.text
    data=json.loads(data)
    return (data['accounts'][0]['accountID'])

