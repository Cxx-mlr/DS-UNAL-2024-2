from __future__ import annotations

from typing_extensions import Optional

from Date import Date
from Time import Time


class DateTime(Date, Time):
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
    ) -> DateTime:
        Date.__init__(self, year, month, day)
        Time.__init__(self, hour, minute, second)

    def get_date(self) -> Date:
        return self

    def get_time(self) -> Time:
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other: object):
        return not self.__eq__(other)

    def to_csv(self) -> str:
        return f"{Date.to_csv(self)} {Time.to_csv(self)}"

    @classmethod
    def from_csv(cls, csv_string: str) -> DateTime:
        parts = csv_string.split()
        if len(parts) != 6:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 6 partes separadas por espacios, pero se obtuvieron {len(parts)} partes: {parts}"
            )

        try:
            date = Date.from_csv(" ".join(parts[:3]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'Date' de las partes {parts[2:5]}. Error: {e}"
            )

        try:
            time = Time.from_csv(" ".join(parts[3:]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'Time' de las partes {parts[2:5]}. Error: {e}"
            )

        return cls(
            year=date.get_year(),
            month=date.get_month(),
            day=date.get_day(),
            hour=time.get_hour(),
            minute=time.get_minute(),
            second=time.get_second(),
        )

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
