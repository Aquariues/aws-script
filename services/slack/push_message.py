import requests
import json
from settings.config import CONFIG

def send_slack_message(message):
    payload = {"text": message}  
    response = requests.post(CONFIG.SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")
