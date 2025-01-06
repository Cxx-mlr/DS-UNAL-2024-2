from __future__ import annotations

from InventoryItem import InventoryItem

from Date import Date

from contextlib import suppress

from Session import Session


class Researcher(Session):
    def display_inventory(self):
        for equipment in self._user_inventory.get_equipments():
            print(equipment, end="", flush=True)

    def add_equipment(self):
        print()
        print("Ingrese los datos del equipo")
        name = input("nombre: ")
        serial_number = int(input("número de placa: "))
        date = input("fecha de compra (dd-mm-aaaa): ").split("-")
        price = int(input("valor de compra: "))

        if len(date) == 3:
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])
        else:
            day, month, year = 1, 1, 2000

        item = InventoryItem(
            username=self._user.get_name(),
            user_id=self._user.get_id(),
            name=name,
            serial_number=serial_number,
            purchase_date=Date(
                day=day,
                month=month,
                year=year
            ),
            price=price
        )

        self._user_add_requests.add(item)

        self._user_add_requests.sort()
        self._user_add_requests.save_to_file(filename="Control_de_cambios.txt")

    def delete_equipment(self):
        print()
        print("Ingrese los datos del equipo")
        serial_number = int(input("número de placa: "))
        reason = input("razón: ")

        item_index = self._user_inventory.find(
            lambda item: item.get_serial_number() == serial_number
        )
        if item_index == -1:
            print(f"No se ha encontrado un equipo con el número de placa {serial_number}")
            return
        
        self._user_delete_requests.add(
            self._user_inventory.get_items()[item_index]
        )

        self._user_delete_requests.sort()
        self._user_delete_requests.save_to_file(filename="Control_de_cambios.txt")

    def requests_status(self):
        add_requests = self._user_add_requests
        delete_requests = self._user_delete_requests

        print(self._user_changelog)

    def save_inventory(self):
        self._user_inventory.save_to_file(
            filename=f"{self._user.get_name()} {self._user.get_id()}2.txt",
            equipment=True
        )

    def display_menu(self):
        options = [
            ("Consultar equipo en inventario", self.display_inventory),
            ("Solicitar adición de equipo", self.add_equipment),
            ("Solicitar eliminación de equipo", self.delete_equipment),
            ("Consultar estado de solicitudes", self.requests_status),
            ("Generar información de inventario", self.save_inventory)
        ]

        for i, option in enumerate(options, start=1):
            option_message, _ = option

            print(f"{i}. {option_message}")
        print()

        choice = None
        while True:
            with suppress(Exception):
                choice = int(input("Seleccione una opción: "))

            if choice not in range(1, len(options) + 1):
                print("[red](Opción incorrecta)[/]")
                print()
            else:
                break

        func = options[choice - 1][1]
        func()