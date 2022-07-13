from dataclasses import asdict, dataclass
from time import time



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
        return asdict(self)
    
    @staticmethod
    def from_dict(data):
        return ScheduleRequest(**data)
    def get_start_time(self):
        return time.ctime(self.start_time)