from __future__ import annotations
from rich import print

from utils import console, ask_in_range, ask_integer
from Session import Session
from contextlib import suppress
from InventoryItem import InventoryItem
from Date import Date
from Time import Time
from Credentials import Credentials
from Equipment import Equipment
from User import User

from ChangelogEntry import ChangelogEntry

class Administrator(Session):
    def display_inventory(self):
        for item in self._user_inventory:
            print(item.get_equipment())

    def add_equipment(self):
        print()
        print("[green]Ingrese los datos solicitados[/]")

        equipment = Equipment.ask()

        item = InventoryItem(
            username=self._user.get_name(),
            user_id=self._user.get_id(),
            name=equipment.get_name(),
            serial_number=equipment.get_serial_number(),
            purchase_date=equipment.get_purchase_date(),
            price=equipment.get_price(),
        )

        with self._inventory as inventory:
            inventory.add(item)
            inventory.sort().save_to_file(filename="InventarioGeneral.txt")

    def delete_equipment(self):
        print()
        with self._inventory as inventory, self._user_inventory as user_inventory:
            indexes = user_inventory.choose(self, rule="Seleccione uno o varios equipos")
            items = tuple(user_inventory[index] for index in indexes)

            inventory.filter(
                lambda item: item not in items
            ).save_to_file(filename="InventarioGeneral.txt")

    def add_user(self):
        print()
        print("[green]Ingrese los datos del usuario[/]")

        credentials = Credentials.ask()
        user = User.ask()

        with self._credentials_list as credentials_list:
            credentials_list.add(credentials)
            credentials_list.save_to_file(filename="Password.txt")

        with self._users as users:
            users.add(user)
            users.save_to_file(filename="Empleados.txt")

    def delete_user(self):
        print()
        with self._credentials_list as credentials_list, self._users as users:
            indexes = credentials_list.choose(self)
            selected_credentials = tuple(credentials_list[index] for index in indexes)
            selected_user_ids = tuple(credentials.get_user_id() for credentials in selected_credentials)
            
            credentials_list.filter(
                lambda credentials: credentials not in selected_credentials
            ).save_to_file(filename="Password.txt")

            users.filter(
                lambda user: user.get_id() not in selected_user_ids
            ).save_to_file(filename="Empleados.txt")

    def change_user_password(self):
        print()
        with self._credentials_list as credentials_list, self._users as users:
            indexes = credentials_list.choose(self)
            for index in indexes:
                current_credentials = credentials_list[index]
                current_user = users.find(
                    lambda user: user.get_id() == current_credentials.get_user_id()
                )
                print(f"\n{current_user.get_name()} {current_user.get_id()}")
                print("[blue]Ingrese una nueva contraseña: [/]", end="", flush=True)
                password = input("")

                credentials_list.find(
                    lambda credentials: credentials.get_user_id() == current_credentials.get_user_id()
                ).set_password(
                    password
                )

            credentials_list.save_to_file(filename="Password.txt")

    def manage_requests(self):
        print()
        with self._add_requests as add_requests:
            indexes = add_requests.choose(
                session=self,
                rule="Seleccione una o varias solicitudes",
                request=True,
                what="agregar"
            )

        options = []
        with self._add_requests as add_requests:
            for item in add_requests:
                equipment = item.get_equipment()
                item_repr = (
                    f"[cyan]{item.get_username()} solicita agregar el equipo "
                    f"{equipment.get_name()} {equipment.get_serial_number()}[/] [[green]${equipment.get_price()}[/]]"
                )
                options.append(
                    (item_repr, "agregar", item)
                )

        with self._delete_requests as delete_requests:
            for item in delete_requests:
                equipment = item.get_equipment()
                item_repr = (
                    f"[cyan]{item.get_username()} solicita eliminar el equipo "
                    f"{equipment.get_name()} {equipment.get_serial_number()} con costo de[/] [[green]{equipment.get_price()}[/]]"
                )
                options.append(
                    (item_repr, "eliminar", item)
                )

        print()
        for i, option in enumerate(options, start=1):
            request_repr, _, _ = option
            print(f"{i}. {request_repr}")

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
        
        item: InventoryItem
        request_repr, what, item = options[choice - 1]

        print(f"\n{request_repr}")
        print("1. [green]Aprobar solicitud[/]")
        print("2. [red]Rechazar solicitud[/]")
        print("3. [red]Salir[/]")
        print()

        request_choice = None
        while True:
            with suppress(Exception):
                request_choice = int(input("Seleccione una opción: "))

            if request_choice not in range(1, 4):
                print("[red](Opción incorrecta)[/]")
            else:
                break

        if what == "agregar":
            with self._changelog as changelog:
                entry = ChangelogEntry(
                    user_id=item.get_user_id(),
                    serial_number=item.get_serial_number(),
                    what="agregar",
                    date=Date.now(),
                    time=Time.now()
                )
                changelog.add(entry)
                changelog.save_to_file(filename="Control_de_cambios.txt")

            with self._inventory as inventory:
                inventory.add(item)
                inventory.sort()
                inventory.save_to_file(filename="InventarioGeneral.txt")
            with self._add_requests as add_requests:
                add_requests.delete(
                    lambda l_item: (
                        l_item.get_user_id() == item.get_user_id()
                        and l_item.get_serial_number() == item.get_serial_number()
                    )
                )
                add_requests.save_to_file(filename="Solicitudes_agregar.txt")
        elif what == "eliminar":
            with self._changelog as changelog:
                entry = ChangelogEntry(
                    user_id=item.get_user_id(),
                    serial_number=item.get_serial_number(),
                    what="eliminar",
                    date=Date.now(),
                    time=Time.now()
                )
                changelog.add(entry)
                changelog.save_to_file(filename="Control_de_cambios.txt")
            with self._inventory as inventory:
                inventory.delete(
                    lambda l_item: (
                        l_item.get_user_id() == item.get_user_id()
                        and l_item.get_serial_number() == item.get_serial_number()
                    )
                )
                inventory.save_to_file(filename="InventarioGeneral.txt")
            with self._delete_requests as delete_requests:
                delete_requests.delete(
                    lambda l_item: (
                        l_item.get_user_id() == item.get_user_id()
                        and l_item.get_serial_number() == item.get_serial_number()
                    )
                )
                delete_requests.save_to_file(filename="Solicitudes_eliminar.txt")

    def generate_user_inventory_info(self):
        print()
        print("Seleccione un usuario para generar inventario")
        user_ids = [user.get_user_id() for user in self._credentials_list]
        users = self._users.filter(lambda user: user.get_id() in user_ids)

        options = [
            (f"{user.get_name()} {user.get_id()}", user.get_id()) for user in users
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

        user_repr, user_id = options[choice - 1]

        with self._inventory as inventory:
            inventory.filter(lambda item: item.get_user_id() == user_id).save_to_file(
                filename=f"{user_repr}.txt", only_equipment=True
            )

    def display_menu(self):
        options = [
            ("Consultar equipo en inventario", self.display_inventory),
            ("Agregar equipo", self.add_equipment),
            ("Eliminar equipo", self.delete_equipment),
            ("Registrar usuario", self.add_user),
            ("Eliminar usuario", self.delete_user),
            ("Cambiar contraseña de un usuario", self.change_user_password),
            ("Administrar solicitudes", self.manage_requests),
            (
                "Generar información de inventario de un usuario",
                self.generate_user_inventory_info,
            ),
        ]

        for i, option in enumerate(options, start=1):
            option_message, _ = option

            print(f"{i}. {option_message}")
        print()

        choice = ask_in_range(
            range_=range(1, len(options) + 1),
            variadic=False,
            msg="Seleccione una opción: ",
            err_msg=f"Por favor ingrese un número entre 1 y {len(options)}"
        )

        options[choice - 1][1]()