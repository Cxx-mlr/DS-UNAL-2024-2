from __future__ import annotations

from datetime import date

class Date:
    def __init__(self, day: int = 1, month: int = 1, year: int = 2000) -> Date:
        self.__day = day
        self.__month = month
        self.__year = year

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

    def __str__(self) -> str:
        return date(year=self.__year, month=self.__month, day=self.__day).strftime("%d-%m-%y")