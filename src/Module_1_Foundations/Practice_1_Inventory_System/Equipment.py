from __future__ import annotations

from rich import print
from utils import console, ask_integer

from Date import Date

class Equipment:
    def __init__(self,
                 name: str, 
                 serial_number: int, 
                 purchase_date: Date, 
                 price: int) -> Equipment:
        self.__name = name
        self.__serial_number = int(serial_number)
        self.__purchase_date = purchase_date
        self.__price = int(price)

    @classmethod
    def ask(cls) -> Equipment:
        console.rule("Equipo")
        print("[blue]Nombre: [/]", end="", flush=True)
        name = input("")
        serial_number = ask_integer("Número de placa: ", "Por favor, proporcione un número de placa válido")
        purchase_date = Date.ask("Fecha de compra (dd-mm-aa): ", "Por favor, proporcione una fecha válida.")
        price = ask_integer("Valor de compra: ", "Por favor, proporcione un valor de compra válido")

        return cls(
            name=name,
            serial_number=serial_number,
            purchase_date=purchase_date,
            price=price
        )

    def get_name(self) -> str:
        return self.__name
    
    def get_serial_number(self) -> int:
        return self.__serial_number
    
    def get_purchase_date(self) -> Date:
        return self.__purchase_date
    
    def get_price(self) -> int:
        return self.__price
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Equipment):
            return self.__dict__ == other.__dict__
        return False
    
    def __ne__(self, other: object):
        return not self.__eq__(other)

    def to_csv(self) -> str:
        purchase_date = f"{self.__purchase_date.get_day()} {self.__purchase_date.get_month()} {self.__purchase_date.get_year()}"
        return f"{self.__name} {self.__serial_number} {purchase_date} {self.__price}"

    @staticmethod
    def from_csv(csv_string: str) -> Equipment:
        parts = csv_string.strip().split(" ")
        name = parts[0]
        serial_number = int(parts[1])
        day, month, year = map(int, parts[2:5])
        purchase_date = Date(day=day, month=month, year=year)
        price = int(parts[5])
        return Equipment(name=name, serial_number=serial_number, purchase_date=purchase_date, price=price)

    def __str__(self) -> str:
        return self.to_csv()