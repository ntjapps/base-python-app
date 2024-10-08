import os
import requests
from dotenv import load_dotenv

load_dotenv()

app_url = os.environ.get("APP_URL")


def getAccessToken(scope=None):
    url = app_url + "/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
        "scope": scope
    }

    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise Exception("Failed to get access token")
    else:
        return response.json()['access_token']


def postApiEndpoint(endpoint, data=None, scope=None):
    url = app_url + endpoint
    token = getAccessToken(scope)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    req = requests.post(url, json=data, headers=headers)

    return req
