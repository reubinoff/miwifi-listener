from fastapi import FastAPI, Request
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every
from fastapi.logger import logger
import aiohttp
import time
import asyncio

from listener.router.router_model import Router
from listener.models import ScheduleRequest

app = FastAPI()

ROUTER_IP = "192.168.31.1"
ROUTER_PASSWORD = "noayairitamar"

URL = "https://func.listener.reubinoff.com/api/miwifi_scheduler"
# URL = "http://localhost:7071/api/miwifi_scheduler"

DEVICES = {
    "TV": "D4:5E:EC:A0:82:C5"
}

async def get_next_job():
   async with aiohttp.ClientSession() as session:
        async with session.put(URL) as response:
            if response.status != 200:
                raise Exception("Job not found")
            return await response.json()


@app.on_event("startup")
@repeat_every(seconds=2)  # 1 hour
async def get_next_job_task() -> None:
    try:
        job = await get_next_job()
        await handler_req(job)
    except Exception as e:
        logger.error(e)
        return
    
async def handler_req(scheduler_request: ScheduleRequest):
    print(scheduler_request)
    req = ScheduleRequest.from_dict(scheduler_request)
    router = Router(ROUTER_IP)
    status_login = router.login(ROUTER_PASSWORD)
    if status_login is True:
        print("Logged in")
    else:
        raise ("Auth Failed")
    

    router.toggle_device_connection( DEVICES[req.device], True)
    await asyncio.sleep(req.duration_in_min * 60)
    router.toggle_device_connection( DEVICES[req.device], False)
    router.logout()


@app.post("/request")
async def add_equest(request: Request):
    time_offset = int(request.query_params["time_offset"] if "time_offset" in request.query_params else "0")
    req = {"username": "test", "start_time": time.time() + time_offset*60, "duration_in_min": 1}
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=req) as response:
            if response.status != 200:
                return "Error"
            return await response.text()