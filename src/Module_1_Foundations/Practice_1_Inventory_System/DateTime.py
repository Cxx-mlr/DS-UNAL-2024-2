from __future__ import annotations

from Date import Date
from Time import Time

class DateTime(Date, Time):
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> DateTime:
        Date.__init__(self, year, month, day)
        Time.__init__(self, hour, minute, second)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.__dict__ == other.__dict__
        return False
    
    def __ne__(self, other: object):
        return not self.__eq__(other)

    @classmethod
    def now(cls) -> DateTime:
        date = Date.now()
        time = Time.now()
        return cls(
            year=date.get_year(),
            month=date.get_month(),
            day=date.get_day(),
            hour=time.get_hour(),
            minute=time.get_minute(),
            second=time.get_second(),
        )