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

    def __str__(self):
        return f"[yellow]Nombre:[/] {self.__name}" \
               f"\n[yellow]ID:[/] {self.__id}" \
               f"\n[yellow]Fecha de nacimiento:[/] {self.__birth_date}, " \
               f"\n[yellow]Ciudad de nacimiento:[/] {self.__birth_city}" \
               f"\n[yellow]Número de teléfono:[/] {self.__phone_number}, " \
               f"\n[yellow]Email:[/] {self.__email}" \
               f"\n[yellow]Address:[/] {self.__address}"
