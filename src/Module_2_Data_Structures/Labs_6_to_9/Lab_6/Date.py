from __future__ import annotations
from rich import print

from typing_extensions import Optional
from datetime import datetime, timezone, date


class Date:
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
    ) -> None:
        self.__year = year
        self.__month = month
        self.__day = day

    @classmethod
    def ask(cls, prompt: str, error_message: str) -> Date:
        while True:
            day, month, year = None, None, None
            try:
                print(f"[blue]{prompt}[/]", end="", flush=True)
                user_input = input("").strip()

                parts = user_input.split("-")
                if len(parts) != 3:
                    raise ValueError(
                        f"La entrada debe contener exactamente tres partes separadas por '-', pero se obtuvieron {len(parts)} parte(s): {parts}"
                    )

                day_str, month_str, year_str = parts

                try:
                    day = int(day_str)
                except ValueError:
                    raise ValueError(f"El valor del día '{day_str}' no es un entero válido.")

                try:
                    month = int(month_str)
                except ValueError:
                    raise ValueError(
                        f"El valor del mes '{month_str}' no es un entero válido."
                    )

                try:
                    year = int(year_str)
                except ValueError:
                    raise ValueError(f"El valor del año '{year_str}' no es un entero válido.")

                if not (1 <= day <= 31):
                    raise ValueError(f"El día debe estar entre 1 y 31, pero se obtuvo {day}.")
                if not (1 <= month <= 12):
                    raise ValueError(
                        f"El mes debe estar entre 1 y 12, pero se obtuvo {month}."
                    )
                if year <= 1900:
                    raise ValueError(f"El año debe ser mayor que 1900, pero se obtuvo {year}.")

            except ValueError as ve:
                print()
                print(f"[yellow]{ve}[/]")
                print(f"[yellow]{error_message}[/]")
            except Exception as e:
                print()
                print(f"[yellow]Unexpected error: {e}[/]")
                print(f"[yellow]{error_message}[/]")
            else:
                break

        return cls(year=year, month=month, day=day)

    @classmethod
    def now(cls) -> Date:
        now = datetime.now(timezone.utc)
        return cls(day=now.day, month=now.month, year=now.year)

    def set_day(self, day: int):
        self.__day = day

    def set_month(self, month: int):
        self.__month = month

    def set_year(self, year: int):
        self.__year = year

    def get_day(self) -> Optional[int]:
        return self.__day

    def get_month(self) -> Optional[int]:
        return self.__month

    def get_year(self) -> Optional[int]:
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
        parts = csv_string.strip().split()
        if len(parts) != 3:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 3 partes separadas por espacios, pero se obtuvieron {len(parts)} partes: {parts}"
            )

        try:
            day = int(parts[0]) if parts[0] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'día' a un entero. Valor proporcionado: {parts[0]}"
            )

        try:
            month = int(parts[1]) if parts[1] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'mes' a un entero. Valor proporcionado: {parts[1]}"
            )

        try:
            year = int(parts[2]) if parts[2] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'año' a un entero. Valor proporcionado: {parts[2]}"
            )

        return Date(year=year, month=month, day=day)

    def __repr__(self) -> str:
        return (
            f"Date("
            f"year={self.__year}"
            f"month={self.__month}, "
            f"day={self.__day}, "
            f")"
        )

    def __str__(self) -> str:
        fmt = "-".join(
            (
                "None" if self.__day is None else "%d",
                "None" if self.__month is None else "%m",
                "None" if self.__year is None else "%y",
            )
        )
        return date(year=self.__year, month=self.__month, day=self.__day).strftime(fmt)
