from dataclasses import dataclass
from functools import lru_cache
import logging
import os
import azure.functions as func
import json
from function.scheduler_manager import SchedulerManager, ScheduleRequest





@lru_cache
def _get_client() -> SchedulerManager:
    # return SchedulerManager(os.environ["AZURE_STORAGE_CONNECTION_STRING"])
    return SchedulerManager("DefaultEndpointsProtocol=https;AccountName=miwifischeduler;AccountKey=Ecv3jdmwtMVTsw3MgL5ZXBoakMI5LNmi8b0WFFAb+I0uO9e2jn/RWsP+E6ynlPvH0ohLpyUdYW6J+AStQl+ylg==;EndpointSuffix=core.windows.net")


def _validate_body(body: dict) -> bool:
    if "username" not in body:
        raise Exception(  "Please provide a username")
    if "start_time" not in body:
        raise Exception(  "Please provide a username")
    if "end_time" not in body:
        raise Exception(  "Please provide a username")

    return True

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    if req.method == "POST":
        body = req.get_json()
        try:
            _validate_body(body)
        except Exception as e:
            return func.HttpResponse(status_code=400, body=str(e))
        try:
            s = ScheduleRequest.from_dict(body)
            _get_client().add_scheduler(s)
            return func.HttpResponse(f"schedule added for {s.username}")
        except Exception as e:
            return func.HttpResponse(status_code=400, body=str(e))
    elif req.method == "DELETE":
        body = req.get_json()
        _get_client().drop_all()
        return func.HttpResponse(f"all schedules dropped" )
    elif req.method == "GET":
        name = req.params["name"] if "name" in req.params else None
        a = _get_client().get_all(name)
        return func.HttpResponse(json.dumps({"version": "1.1", "items": a}), mimetype="application/json")
    elif req.method == "PUT":
        a = _get_client().consume_next()
        if a is None:
            return func.HttpResponse(status_code=404, body="no schedule found")
        return func.HttpResponse(json.dumps(a.as_dict()), mimetype="application/json")
    return func.HttpResponse(f"Hello, {req.params}. This HTTP triggered function executed successfully.")

