from __future__ import annotations

from typing_extensions import Optional

from utils import console, ask_integer, ask_string
from Date import Date


class Equipment:
    def __init__(
        self,
        name: Optional[str] = None,
        serial_number: Optional[int] = None,
        purchase_date: Optional[Date] = None,
        price: Optional[int] = None,
    ) -> None:
        self.__name = name
        self.__serial_number = serial_number
        self.__purchase_date = purchase_date
        self.__price = price

    @classmethod
    def ask(cls) -> Equipment:
        console.rule("Equipo")
        name = "_".join(ask_string("Nombre: ").split(" "))
        serial_number = ask_integer(
            "Número de placa: ", "Por favor, proporcione un número de placa válido."
        )
        purchase_date = Date.ask(
            "Fecha de compra (dd-mm-aaaa): ", "Por favor, proporcione una fecha válida."
        )
        price = ask_integer(
            "Valor de compra: ", "Por favor, proporcione un valor de compra válido."
        )

        return cls(
            name=name,
            serial_number=serial_number,
            purchase_date=purchase_date,
            price=price,
        )

    def get_name(self) -> Optional[str]:
        return self.__name

    def get_serial_number(self) -> Optional[int]:
        return self.__serial_number

    def get_purchase_date(self) -> Optional[Date]:
        return self.__purchase_date

    def get_price(self) -> Optional[int]:
        return self.__price

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Equipment):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other: object):
        return not self.__eq__(other)

    def to_csv(self) -> str:
        purchase_date_repr = f"{self.__purchase_date.get_day()} {self.__purchase_date.get_month()} {self.__purchase_date.get_year()}"
        return (
            f"{self.__name} {self.__serial_number} {purchase_date_repr} {self.__price}"
        )

    @staticmethod
    def from_csv(csv_string: str) -> Equipment:
        parts = csv_string.strip().split()

        if len(parts) != 6:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 6 partes separadas por espacios, pero tiene {len(parts)} partes: {parts}"
            )

        try:
            name = parts[0] if parts[0] != "None" else None
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'name' de la cadena CSV. Partes: {parts}"
            )

        try:
            serial_number = int(parts[1]) if parts[1] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'serial_number' a un entero. Valor proporcionado: {parts[1]}"
            )
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'serial_number' de la cadena CSV. Partes: {parts}"
            )

        try:
            purchase_date = Date.from_csv(" ".join(parts[2:5]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'Date' de las partes {parts[2:5]}. Error: {e}"
            )

        try:
            price = int(parts[5]) if parts[5] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'price' a un entero. Valor proporcionado: {parts[5]}"
            )
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'price' de la cadena CSV. Partes: {parts}"
            )

        return Equipment(
            name=name,
            serial_number=serial_number,
            purchase_date=purchase_date,
            price=price,
        )

    def __str__(self) -> str:
        return self.to_csv()
