from __future__ import annotations

from rich import print

from datetime import datetime, timezone, date
from contextlib import suppress

class Date:
    def __init__(self, year: int = 2000, month: int = 1, day: int = 1) -> Date:
        self.__year = year
        self.__month = month
        self.__day = day

    @classmethod
    def ask(cls, msg: str, err_msg: str) -> Date:
        while True:
            day, month, year = None, None, None
            with suppress(Exception):
                print(f"[blue]{msg}[/]", end="", flush=True)
                day, month, year = input("").split("-")
                day = int(day)
                month = int(month)
                year = int(year)

            if day == month == year == None:
                print()
                print(f"[yellow]{err_msg}[/]")
            else:
                break
        
        return cls(
            year=year,
            month=month,
            day=day
        )

    @classmethod
    def now(cls) -> Date:
        now = datetime.now(timezone.utc)
        return cls(
            day=now.day,
            month=now.month,
            year=now.year
        )

    def set_day(self, day: int):
        self.__day = day

    def set_month(self, month: int):
        self.__month = month

    def set_year(self, year: int):
        self.__year = year

    def get_day(self) -> int:
        return self.__day

    def get_month(self) -> int:
        return self.__month

    def get_year(self) -> int:
        return self.__year
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.__dict__ == other.__dict__
        return False
    
    def __ne__(self, other: object):
        return not self.__eq__(other)
    
    def to_csv(self):
        return f"{self.__day} {self.__month} {self.__year}"
    
    @staticmethod
    def from_csv(csv_string: str) -> Date:
        parts = csv_string.split(" ")
        year = int(parts[2])
        month = int(parts[1])
        day = int(parts[0])

        return Date(
            year=year,
            month=month,
            day=day
        )
    
    def __repr__(self) -> str:
        return (
            f"Date("
            f"year={self.__year}"
            f"month={self.__month}, "
            f"day={self.__day}, "
            f")"
        )

    def __str__(self) -> str:
        return date(
            year=self.__year,
            month=self.__month,
            day=self.__day
        ).strftime("%d-%m-%y")