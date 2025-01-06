from __future__ import annotations

from datetime import datetime, time, timezone


class Time:
    def __init__(self, hour: int, minute: int, second: int) -> Time:
        self.__hour = hour
        self.__minute = minute
        self.__second = second

    @classmethod
    def now(cls) -> Time:
        now = datetime.now(timezone.utc)
        return cls(
            hour=now.hour,
            minute=now.minute,
            second=now.second
        )

    def get_hour(self) -> int:
        return self.__hour
    
    def get_minute(self) -> int:
        return self.__minute
    
    def get_second(self) -> int:
        return self.__second
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Time):
            return self.__dict__ == other.__dict__
        return False
    
    def __ne__(self, other: object):
        return not self.__eq__(other)
    
    def to_csv(self):
        return f"{self.__hour} {self.__minute} {self.__second}"
    
    @staticmethod
    def from_csv(csv_string: str) -> Time:
        parts = csv_string.split(" ")
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2])

        return Time(
            hour=hour,
            minute=minute,
            second=second
        )
    
    def __repr__(self) -> str:
        return (
            f"Time("
            f"hour={self.__hour}, "
            f"minute={self.__minute}, "
            f"second={self.__second}"
            f")"
        )

    def __str__(self) -> str:
        return time(
            hour=self.__hour,
            minute=self.__minute,
            second=self.__second
        ).strftime("%H-%M-%S")