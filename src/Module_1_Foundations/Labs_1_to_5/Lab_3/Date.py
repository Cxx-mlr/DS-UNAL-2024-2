from __future__ import annotations

import datetime

class Date:
    def __init__(self, day: int = 1, month: int = 1, year: int = 2000) -> Date:
        self.__day = day
        self.__month = month
        self.__year = year

    # def to_csv(self) -> str:
    #     return " ".join(
    #         (
    #             self.__day,
    #             self.__month,
    #             self.__year
    #         )
    #     )
    
    # @staticmethod
    # def from_csv(csv_string: str) -> Date:
    #     parts = csv_string.split(" ")

    #     if len(parts) != 3:
    #         raise ValueError("CSV string must contain exactly three parts")
        
    #     (
    #         day,
    #         month,
    #         year
    #     ) = parts

    #     return Date(
    #         day=day,
    #         month=month,
    #         year=year
    #     )

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
    
    def __repr__(self) -> str:
        return (
            f"Date("
            f"day={self.__day}, "
            f"month={self.__month}, "
            f"year={self.__year}"
            f")"
        )

    def __str__(self) -> str:
        return datetime.date(
            year=self.__year,
            month=self.__month,
            day=self.__day
        ).strftime("%d-%m-%y")