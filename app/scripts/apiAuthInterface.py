import os
import requests

webhook_endpoint = os.environ.get("WEBHOOK_ENDPOINT")


def getAccessToken():
    url = webhook_endpoint + "/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
    }

    response = requests.post(url, json=data)

    return response.json()["access_token"]
