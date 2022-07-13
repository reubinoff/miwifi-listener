from fastapi import FastAPI
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every
from fastapi.logger import logger
import aiohttp


app = FastAPI()

URL = "https://miwifi-service.azurewebsites.net/api/miwifi_scheduler"
# URL = "http://localhost:7071/api/miwifi_scheduler"

async def get_all_jobs():
   async with aiohttp.ClientSession() as session:
        async with session.put(URL) as response:
            if response.status == 404:
                return "No jobs found"
            return await response.json()


@app.on_event("startup")
@repeat_every(seconds=2)  # 1 hour
async def remove_expired_tokens_task() -> None:
    a= await get_all_jobs()
    logger.error( a)