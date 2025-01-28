from __future__ import annotations

from utils import console, ask_string, format_for_csv, format_from_csv
from typing_extensions import Optional


class Address:
    def __init__(
        self,
        street: Optional[str] = None,
        nomenclature: Optional[str] = None,
        neighborhood: Optional[str] = None,
        city: Optional[str] = None,
        building: Optional[str] = None,
        apartment: Optional[str] = None,
    ) -> None:
        self.__street = street
        self.__nomenclature = nomenclature
        self.__neighborhood = neighborhood
        self.__city = city
        self.__building = building
        self.__apartment = apartment

    def to_csv(self) -> str:
        return (
            f"{format_for_csv(self.__street)} "
            f"{format_for_csv(self.__nomenclature)} "
            f"{format_for_csv(self.__neighborhood)} "
            f"{format_for_csv(self.__city)} "
            f"{format_for_csv(self.__building)} "
            f"{format_for_csv(self.__apartment)}"
        )

    @classmethod
    def from_csv(cls, csv_string: str) -> Address:
        parts = csv_string.strip().split()
        if len(parts) != 6:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 6 partes separadas por espacios, pero tiene {len(parts)} partes: {parts}"
            )

        try:
            formatted_parts = list(map(format_from_csv, parts))
        except Exception as e:
            raise ValueError(
                f"Se produjo un error durante el formateo de las partes: {e}"
            )

        street, nomenclature, neighborhood, city, building, apartment = formatted_parts

        return cls(
            street=street,
            nomenclature=nomenclature,
            neighborhood=neighborhood,
            city=city,
            building=building,
            apartment=apartment,
        )

    @classmethod
    def ask(cls) -> Address:
        console.rule("Dirección")

        street = ask_string("Calle: ")
        nomenclature = ask_string("Nomenclatura: ")
        neighborhood = ask_string("Barrio: ")
        city = ask_string("Ciudad: ")
        building = ask_string("Edificio: ")
        apartment = ask_string("Apartamento: ")

        return cls(
            street=street,
            nomenclature=nomenclature,
            neighborhood=neighborhood,
            city=city,
            building=building,
            apartment=apartment,
        )

    def set_street(self, street: str):
        self.__street = street

    def set_nomenclature(self, nomenclature: str):
        self.__nomenclature = nomenclature

    def set_neighborhood(self, neighborhood: str):
        self.__neighborhood = neighborhood

    def set_city(self, city: str):
        self.__city = city

    def set_building(self, building: str):
        self.__building = building

    def set_apartment(self, apartment: str):
        self.__apartment = apartment

    def get_street(self) -> str:
        return self.__street

    def get_nomenclature(self) -> str:
        return self.__nomenclature

    def get_neighborhood(self) -> str:
        return self.__neighborhood

    def get_city(self) -> str:
        return self.__city

    def get_building(self) -> str:
        return self.__building

    def get_apartment(self) -> str:
        return self.__apartment

    def __repr__(self) -> str:
        return (
            f"Address(street={self.__street!r}, "
            f"nomenclature={self.__nomenclature!r}, "
            f"neighborhood={self.__neighborhood!r}, "
            f"city={self.__city!r}, "
            f"building={self.__building!r}, "
            f"apartment={self.__apartment!r}"
            f")"
        )

    def __str__(self):
        parts = []

        if self.__street:
            parts.append(f"{self.__street}")
        if self.__nomenclature:
            parts.append(f"No. {self.__nomenclature}")
        if self.__neighborhood:
            parts.append(f"en {self.__neighborhood}")
        if self.__city:
            parts.append(f", {self.__city}")
        if self.__building:
            parts.append(f", Edificio {self.__building}")
        if self.__apartment:
            parts.append(f", Apartmento {self.__apartment}")

        return " ".join(parts) if parts else "Null"
