import logging
import requests
import azure.functions as func
import datetime
import jwt
import json

# URL = "http://localhost:7071/api/miwifi_users"
URL = "https://miwifi-service.azurewebsites.net/api/miwifi_users"

PASS = {
    "admin": "hello",
    "noa": "noa1",
    "yair": "yair2",
    "itamar": "itamar3",
}
SECRET_KEY = "python_jwt"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger for Login')
    # login for user
    #get username from body
    username = req.get_json()['username']
    password = req.get_json()['password']
    # get users from service:
    
    response = requests.get(URL)
    if response.status_code != 200:
        return func.HttpResponse(f"Error: {response.status_code}", status_code=response.status_code)
    print(response.text)
    users = response.json()
    if username in users["users"]:
        if PASS[username] == password:
            response = {
                "username": username,
                "token": get_jwt(username)
            }
            return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
        else:
            return func.HttpResponse(f"Wrong password for {username}", status_code=401)


def get_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')