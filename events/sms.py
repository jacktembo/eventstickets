import requests
import json


def send_sms(phone_number, message):
    url = "https://probasesms.com/api/json/multi/res/bulk/sms"
    payload = json.dumps({
        "username": "All1Zed@12$$", "password": "All1Zed@sms12$$",
        "recipient": [int('26' + phone_number)], "senderid": "All1Zed", "message": message,
        "source": "All1Zed"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


