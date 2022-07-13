import logging
from dataclasses import dataclass, asdict
import threading
import datetime
from typing import List, Optional
import uuid
import time

from function.miwifi_scheduler.storage.azure_storage import BlobManager

DEVICES = {
    "TV": "TV"
}
TOTAL_SCHEDULE_PER_DAY_IN_MIN = 60
THRESHOLD_TIME_IN_SECONDS = 30
logger = logging.getLogger(__name__)

@dataclass
class ScheduleRequest:
    username: str
    start_time: float
    duration_in_min: int
    utc_offset_in_seconds: int = 10800 # datetime.datetime.now(tzlocal()).utcoffset().total_seconds()
    device: str = "TV"
    id: int = None
    consumed: bool = False

    def as_dict(self):
        # for key, value in self.__dict__.items():
        #     if isinstance(value, datetime.datetime):
        #         self.__dict__[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        return asdict(self)
    
    @staticmethod
    def from_dict(data):
        # data["start_time"] = datetime.datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        # data["end_time"] = datetime.datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S")
        return ScheduleRequest(**data)
    def get_start_time(self):
        return time.ctime(self.start_time)
    
    @property
    def request_date(self):
        return datetime.datetime.fromtimestamp( self.start_time).date()

def get_current_time_in_req_tz(schedule_request: ScheduleRequest) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(time.time() + schedule_request.utc_offset_in_seconds)

def get_current_time_in_req_tz_epoc(schedule_request: ScheduleRequest) -> float:
    return time.time() + schedule_request.utc_offset_in_seconds

class SchedulerManager:
    def __init__(self, azure_connection_string, force_clean=False):
        self.scheduler_list_lock = threading.Lock()
        self.client = BlobManager(azure_connection_string)

        self.scheduler_list_lock.acquire()
        if force_clean:
            self.client.drop_db()
            self.client.set_db(str(dict()))
        data = self.client.get_db()
      
        if "scheduler" not in data:
            data["scheduler"] = {}
            self.client.set_db(data)
        self.scheduler_list_lock.release()

    def get_all(self, username=None):
        self.scheduler_list_lock.acquire()
        data = self.client.get_db()
        self.scheduler_list_lock.release()
        if username is None:
            return data["scheduler"]
        return data["scheduler"][username] if username in data["scheduler"] else []
    def drop_all(self):
        self.scheduler_list_lock.acquire()
        try:
            self.client.drop_db()
            self.client.set_db(str(dict()))
            data = self.client.get_db()
        
            if "scheduler" not in data:
                data["scheduler"] = {}
                self.client.set_db(data)
        finally:
            self.scheduler_list_lock.release()

    def _clean_not_today_requests(self, username_schdule:List[ScheduleRequest] )-> List[ScheduleRequest]:
        results = []
        for sch in username_schdule:
            if sch.request_date == get_current_time_in_req_tz(sch).date():
                results.append(sch)
        return results
    def _get_total_duration_in_min(self, username_schdule:List[ScheduleRequest] )-> int:
        return sum(sch.duration_in_min for sch in username_schdule)
        

    def _check_daily_duration(self, username_schdule: List[ScheduleRequest]) -> bool:
        if self._get_total_duration_in_min(username_schdule) >= TOTAL_SCHEDULE_PER_DAY_IN_MIN:
            return False
        return True
    
    def _check_username_existance(self, data, username) -> List[ScheduleRequest]:
        if username not in data["scheduler"]:
            data["scheduler"][username] = []
        
        items: List[ScheduleRequest] = [ScheduleRequest.from_dict(item) for item in data["scheduler"][username]]
        return self._clean_not_today_requests(items)
    

    def add_scheduler(self, scheduler:ScheduleRequest) -> bool:
        
        
        if scheduler.start_time < (time.time() - THRESHOLD_TIME_IN_SECONDS):
            raise Exception("Start time is in the past")
  
        if scheduler.request_date != get_current_time_in_req_tz(scheduler).date():
            raise Exception("Start time is not today")


        self.scheduler_list_lock.acquire()
        try:
            data = self.client.get_db()
            username_schdule = self._check_username_existance(data, scheduler.username)
            if not self._check_daily_duration(username_schdule):
                logger.info("Daily duration exceeded for user: {}".format(scheduler.username))
                raise Exception("Daily duration exceeded for user: {}".format(scheduler.username))
            scheduler.id = uuid.uuid4().int
            username_schdule.append(scheduler)
            data["scheduler"][scheduler.username] = [s.as_dict() for s in username_schdule]
            self.client.set_db(data)
        finally:
            self.scheduler_list_lock.release()
        return True



    def get_scheduler_by_name(self, username) -> List[ScheduleRequest]:
        self.scheduler_list_lock.acquire()
        data = self.client.get_db()
        username_schdule = self._check_username_existance(data, username)
  
       
        self.scheduler_list_lock.release()
        return username_schdule

    def _update_consumed_by_id(self, username_schdule:List[ScheduleRequest], id: int) -> List[ScheduleRequest]:
        
        for sch in username_schdule:
            if sch.id == id:
                sch.consumed = True
        return username_schdule
    
    def _update_consume_by_id(self, username_schdule: List[ScheduleRequest], id: int) -> List[ScheduleRequest]:
        for sch in username_schdule:
            if sch.id == id:
                sch.consumed = True
        return username_schdule
    def consume_scheduler_by_username(self, username) -> Optional[ScheduleRequest]:
        self.scheduler_list_lock.acquire()
        try:
            data = self.client.get_db()
            username_schdule = self._check_username_existance(data, username)
            not_consumed_scheduler = [s for s in username_schdule if not s.consumed and s.start_time <= time.time()]

            order_by_start_time = sorted(not_consumed_scheduler, key=lambda x: x.start_time)
            if len(order_by_start_time) > 0:
                order_by_start_time[0].consumed = True
                data["scheduler"][username] = [s.as_dict() for s in self._update_consume_by_id( username_schdule, order_by_start_time[0].id) ]
                self.client.set_db(data)
                return order_by_start_time[0]
            return None
        finally:
            self.scheduler_list_lock.release()
    
    def consume_next(self) -> Optional[ScheduleRequest]:
        self.scheduler_list_lock.acquire()
        data = self.client.get_db()
        usernames = data["scheduler"].keys()
        self.scheduler_list_lock.release()
        for username in usernames:
            item = self.consume_scheduler_by_username(username)
            if item is not None:
                return item

        return None

if __name__ == "__main__":
    scheduler_manager = SchedulerManager("DefaultEndpointsProtocol=https;AccountName=miwifischeduler;AccountKey=Ecv3jdmwtMVTsw3MgL5ZXBoakMI5LNmi8b0WFFAb+I0uO9e2jn/RWsP+E6ynlPvH0ohLpyUdYW6J+AStQl+ylg==;EndpointSuffix=core.windows.net", force_clean=True)

    a= scheduler_manager.add_scheduler(ScheduleRequest.from_dict({"username": "test", "start_time": time.time(), "duration_in_min": 15}))
    a = scheduler_manager.add_scheduler(ScheduleRequest.from_dict({"username": "test", "start_time": time.time()+60*1, "duration_in_min": 15}))
    a = scheduler_manager.add_scheduler(ScheduleRequest.from_dict({"username": "test", "start_time": time.time()+60*30, "duration_in_min": 15}))
    a = scheduler_manager.add_scheduler(ScheduleRequest.from_dict({"username": "test", "start_time": time.time()+60*45, "duration_in_min": 15}))
    # a = scheduler_manager.add_scheduler(ScheduleRequest.from_dict({"username": "test", "start_time": time.time()+60*60, "duration_in_min": 15}))
    
    b = scheduler_manager.consume_next()
    b = scheduler_manager.consume_next()
    counter = 0
    while b is  None:
        print(b)
        b = scheduler_manager.consume_next()
        time.sleep(10)
        print(".")
        counter += 10
    print(counter)
    pass
