from __future__ import annotations

from typing_extensions import Literal

from InventoryItem import InventoryItem
from Date import Date
from Time import Time

class ChangelogEntry:
    def __init__(
            self,
            user_id: int,
            serial_number: int,
            what: Literal["agregar", "eliminar"],
            date: Date,
            time: Time,
            status: str = "PENDING"
    ) -> ChangelogEntry:
        self.__user_id = int(user_id)
        self.__serial_number = serial_number
        self.__what = what
        self.__date = date
        self.__time = time
        self.__status = status

    @classmethod
    def from_item(cls, item: InventoryItem, what: Literal["agregar", "eliminar"]) -> ChangelogEntry:
        return cls(
            user_id=item.get_user_id(),
            serial_number=item.get_serial_number(),
            what=what,
            date=Date.now(),
            time=Time.now()
        )

    def get_user_id(self) -> int:
        return self.__user_id
    
    def get_serial_number(self) -> int:
        return self.__serial_number
    
    def get_action(self) -> str:
        return self.__what
    
    def get_date(self) -> Date:
        return self.__date
    
    def get_time(self) -> Time:
        return self.__time
    
    def get_status(self) -> str:
        return self.__status

    def to_csv(self) -> str:
        return f"{self.__user_id} {self.__serial_number} {self.__what} {self.__date.to_csv()} {self.__time.to_csv()}"
    
    @staticmethod
    def from_csv(csv_string: str) -> ChangelogEntry:
        parts = csv_string.split(" ")
        user_id = int(parts[0])
        serial_number = int(parts[1])
        what = parts[2]

        date = Date.from_csv(" ".join(parts[3:6]))
        time = Time.from_csv(" ".join(parts[6:9]))

        return ChangelogEntry(
            user_id=user_id,
            serial_number=serial_number,
            what=what,
            date=date,
            time=time
        )
    
    def __str__(self) -> str:
        return self.to_csv()