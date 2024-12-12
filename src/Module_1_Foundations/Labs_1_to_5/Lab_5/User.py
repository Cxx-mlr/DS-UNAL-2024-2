from __future__ import annotations


from Date import Date
from Address import Address

from typing_extensions import Optional

class User:
    def __init__(
            self,
            name: str = "",
            id: int = 0,
            birth_date: Optional[Date] = None,
            birth_city: str = "",
            phone_number: int = 0,
            email: str = "",
            address: Optional[Address] = None
    ) -> User:
        self.__name = name
        self.__id = id
        self.__birth_date = birth_date
        self.__birth_city = birth_city
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address

    def to_csv(self) -> str:
        if self.__birth_date:
            birth_date = (
                self.__birth_date.get_day(),
                self.__birth_date.get_month(),
                self.__birth_date.get_year()
            )
        else:
            birth_date = (
                "null", "null", "null"
            )

        if self.__address:
            address = (
                self.__address.get_street(),
                self.__address.get_nomenclature(),
                self.__address.get_neighborhood(),
                self.__address.get_city(),
                self.__address.get_building(),
                self.__address.get_apartment()
            )

        else:
            address = (
                "null", "null", "null", "null", "null", "null"
            )
        
        return " ".join(
            map(
                str,
                (
                    self.__name,
                    self.__id,
                    *birth_date,
                    self.__birth_city,
                    self.__phone_number,
                    self.__email,
                    *address
                )
            )
        ) + "\n"
    
    @staticmethod
    def from_csv(csv_string: str) -> User:
        parts = []

        for part in csv_string.split(" "):
            if part == "null":
                parts.append(None)
            else:
                parts.append(part)

        (
            name,
            id,
            day,
            month,
            year,
            birth_city,
            phone_number,
            email,
            street,
            nomenclature,
            neighborhood,
            city,
            building,
            apartment
        ) = parts

        birth_date = Date(
            day=int(day),
            month=int(month),
            year=int(year)
        )

        address = Address(
            street=street,
            nomenclature=nomenclature,
            neighborhood=neighborhood,
            city=city,
            building=building,
            apartment=apartment
        )

        return User(
            name=name,
            id=int(id),
            birth_date=birth_date,
            birth_city=birth_city,
            phone_number=int(phone_number),
            email=email,
            address=address
        )

    def set_name(self, name: str):
        self.__name = name

    def set_id(self, id: str):
        self.__id = id

    def set_birth_date(self, birth_date: str):
        self.__birth_date = birth_date

    def set_birth_city(self, birth_city: str):
        self.__birth_city = birth_city

    def set_phone_number(self, phone_number: str):
        self.__phone_number = phone_number

    def set_email(self, email: str):
        self.__email = email

    def set_address(self, address: str):
        self.__address = address

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> int:
        return self.__id

    def get_birth_date(self) -> Date:
        return self.__birth_date

    def get_birth_city(self) -> str:
        return self.__birth_city

    def get_phone_number(self) -> int:
        return self.__phone_number

    def get_email(self) -> str:
        return self.__email

    def get_address(self) -> Address:
        return self.__address
    
    def __repr__(self):
        return (
            f"User("
            f"name={self.__name!r}, "
            f"id={self.__id!r}, "
            f"birth_date={self.__birth_date!r}, "
            f"birth_city={self.__birth_city!r}, "
            f"phone_number={self.__phone_number!r}, "
            f"email={self.__email!r}, "
            f"address={self.__address!r}"
            f")"
        )

    def __str__(self):
        return (
            f"[yellow]Nombre:[/] {self.__name}" \
            f"\n[yellow]ID:[/] {self.__id}" \
            f"\n[yellow]Fecha de nacimiento:[/] {self.__birth_date}, " \
            f"\n[yellow]Ciudad de nacimiento:[/] {self.__birth_city}" \
            f"\n[yellow]Número de teléfono:[/] {self.__phone_number}, " \
            f"\n[yellow]Email:[/] {self.__email}" \
            f"\n[yellow]Address:[/] {self.__address}"
        )