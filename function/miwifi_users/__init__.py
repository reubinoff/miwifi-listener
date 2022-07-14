import logging

import azure.functions as func


USERS = [     
    "admin",
    "noa",
    "yair",
    "itamar",
]
def main(req: func.HttpRequest) -> func.HttpResponse:
        # return users list
        return func.HttpResponse(str(USERS))