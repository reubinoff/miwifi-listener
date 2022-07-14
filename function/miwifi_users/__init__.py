import logging

import azure.functions as func
import json

USERS = [     
    "admin",
    "noa",
    "yair",
    "itamar",
]
def main(req: func.HttpRequest) -> func.HttpResponse:
        # return users list
        return func.HttpResponse(json.dumps({"users": USERS}), mimetype="application/json")