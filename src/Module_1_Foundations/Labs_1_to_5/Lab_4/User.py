from __future__ import annotations

from utils import console, ask_integer, ask_string, format_for_csv

from typing_extensions import Optional

from Date import Date
from Address import Address


class User:
    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[int] = None,
        birth_date: Optional[Date] = None,
        birth_city: Optional[str] = None,
        phone_number: Optional[int] = None,
        email: Optional[str] = None,
        address: Optional[Address] = None,
    ) -> User:
        self.__name = name
        self.__id = id
        self.__birth_date = birth_date
        self.__birth_city = birth_city
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address

    @classmethod
    def ask(cls) -> User:
        console.rule("Usuario")

        name: str = ask_string("Nombre: ")
        id = ask_integer("ID: ", "Por favor, proporcione un ID de usuario válido.")
        email: str = ask_string("Email: ")
        birth_date = Date.ask(
            "Fecha de nacimiento (dd-mm-aaaa): ",
            "Por favor, proporcione una fecha válida.",
        )
        birth_city = ask_string("Ciudad de nacimiento: ")
        phone_number = ask_integer(
            "Número de teléfono: ",
            "Por favor, proporcione un número de teléfono válido.",
        )

        print()
        address = Address.ask()

        user = cls(
            name=name,
            id=id,
            birth_date=birth_date,
            birth_city=birth_city,
            phone_number=phone_number,
            email=email,
            address=address,
        )

        return user

    def to_csv(self) -> str:
        if self.__birth_date is None:
            birth_date = Date()
        else:
            birth_date = self.__birth_date

        return " ".join(
            map(
                str,
                (
                    "-".join(self.__name.split()),
                    format_for_csv(self.__id),
                    birth_date.to_csv(),
                    format_for_csv(self.__birth_city),
                    format_for_csv(self.__phone_number),
                    format_for_csv(self.__email),
                    self.__address.to_csv(),
                ),
            )
        )

    @staticmethod
    def from_csv(csv_string: str) -> User:
        parts = csv_string.split()

        if len(parts) != 14:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 13 partes separadas por espacios, pero se obtuvieron {len(parts)} partes: {parts}"
            )

        try:
            name = parts[0] if parts[0] != "None" else None
        except Exception as e:
            raise ValueError(f"No se pudo extraer 'nombre'. Error: {e}")

        try:
            id = int(parts[1]) if parts != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'id' a un entero. Valor proporcionado: {parts[1]}"
            )

        try:
            birth_date = Date.from_csv(" ".join(parts[2:5]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'Date' de las partes {parts[2:5]}. Error: {e}"
            )

        try:
            birth_city = parts[5] if parts[5] != "None" else None
        except Exception as e:
            raise ValueError(f"No se pudo extraer 'ciudad de nacimiento'. Error: {e}")

        try:
            phone_number = int(parts[6]) if parts[6] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'phone_number' a un entero. Valor proporcionado: {parts[6]}"
            )

        try:
            email = parts[7] if parts[7] != "None" else None
        except Exception as e:
            raise ValueError(f"No se pudo extraer 'email'. Error: {e}")

        try:
            address = Address.from_csv(" ".join(parts[8:]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'Address' de las partes {parts[8:]}. Error: {e}"
            )

        return User(
            name=name,
            id=id,
            birth_date=birth_date,
            birth_city=birth_city,
            phone_number=phone_number,
            email=email,
            address=address,
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

    def get_name(self) -> Optional[str]:
        return self.__name

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_birth_date(self) -> Optional[Date]:
        return self.__birth_date

    def get_birth_city(self) -> Optional[str]:
        return self.__birth_city

    def get_phone_number(self) -> Optional[int]:
        return self.__phone_number

    def get_email(self) -> Optional[str]:
        return self.__email

    def get_address(self) -> Optional[Address]:
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
            f"[yellow]Nombre:[/] {self.__name}"
            f"\n[yellow]ID:[/] {self.__id}"
            f"\n[yellow]Fecha de nacimiento:[/] {self.__birth_date}, "
            f"\n[yellow]Ciudad de nacimiento:[/] {self.__birth_city}"
            f"\n[yellow]Número de teléfono:[/] {self.__phone_number}, "
            f"\n[yellow]Email:[/] {self.__email}"
            f"\n[yellow]Address:[/] {self.__address}"
        )
