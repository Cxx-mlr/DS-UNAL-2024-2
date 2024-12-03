from __future__ import annotations

class Address:
    def __init__(
        self,
        street: str = "",
        nomenclature: str = "",
        neighborhood: str = "",
        city: str = "",
        building: str = "",
        apartment: str = ""
    ) -> Address:
        self.__street = street
        self.__nomenclature = nomenclature
        self.__neighborhood = neighborhood
        self.__city = city
        self.__building = building
        self.__apartment = apartment

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