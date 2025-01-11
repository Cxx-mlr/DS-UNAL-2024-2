from __future__ import annotations

from typing_extensions import Optional
from datetime import datetime, time


class Time:
    def __init__(
        self,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
    ) -> Time:
        self.__hour = hour
        self.__minute = minute
        self.__second = second

    @classmethod
    def now(cls) -> Time:
        now = datetime.now()
        return cls(hour=now.hour, minute=now.minute, second=now.second)

    def get_hour(self) -> Optional[int]:
        return self.__hour

    def get_minute(self) -> Optional[int]:
        return self.__minute

    def get_second(self) -> Optional[int]:
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
        parts = csv_string.strip().split()
        if len(parts) != 3:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 3 partes separadas por espacios, pero se obtuvieron {len(parts)} partes: {parts}"
            )

        try:
            hour = int(parts[0]) if parts[0] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'hour' a un entero. Valor proporcionado: {parts[0]}"
            )

        try:
            minute = int(parts[1]) if parts[1] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'minute' a un entero. Valor proporcionado: {parts[1]}"
            )

        try:
            second = int(parts[2]) if parts[2] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'second' a un entero. Valor proporcionado: {parts[2]}"
            )

        return Time(hour=hour, minute=minute, second=second)

    def __repr__(self) -> str:
        return (
            f"Time("
            f"hour={self.__hour}, "
            f"minute={self.__minute}, "
            f"second={self.__second}"
            f")"
        )

    def __str__(self) -> str:
        fmt = "-".join(
            (
                "None" if self.__hour is None else "%H",
                "None" if self.__minute is None else "%M",
                "None" if self.__second is None else "%S",
            )
        )
        return time(
            hour=self.__hour, minute=self.__minute, second=self.__second
        ).strftime(fmt)
