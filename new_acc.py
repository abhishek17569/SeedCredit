import requests
import json

url = "https://fusion.preprod.zeta.in/api/v1/ifi/{{ifiID}}/applications/newIndividual" #ifiID goes here
def new_acc(name,p_no,pan,uid):
    payload = json.dumps({
    "ifiID": "140793",
    "formID": uid,
    "spoolID": "123",
    "individualType": "REAL",
    "salutation": "Mr.",
    "firstName": name,
    "middleName": "",
    "lastName": "Gitika",
    "profilePicURL": "",
    "dob": {
        "year": 1992,
        "month": 7,
        "day": 5
    },
    "gender": "FEMALE",
    "mothersMaidenName": "Rashmi",
    "kycDetails": {
        "kycStatus": "MINIMAL",
        "kycStatusPostExpiry": "string",
        "kycAttributes": {},
        "authData": {
        "PAN": pan
        },
        "authType": "PAN"
    },
    "vectors": [
        {
        "type": "p",
        "value": p_no,
        "isVerified": False
        }
    ],
    "pops": [],
    "customFields": {
        "companyID": [
        1,
        2,
        3
        ]
    },
    "tags": [
        {
        "type": "vbo",
        "value": "swiggy",
        "isVerified": False
        }
    ],
    "source": "postman"
    })
    headers = {
    'Content-Type': 'application/json',
    'X-Zeta-AuthToken': 'Auth Key' ,     # Auth key goes here
    'Cache-Control': 'no-cache'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    return data['individualID']
