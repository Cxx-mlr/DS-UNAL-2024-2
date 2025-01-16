from __future__ import annotations
from rich import print

from Credentials import Credentials
from Equipment import Equipment
from EquipmentList import EquipmentList
from InventoryItem import InventoryItem
from Session import Session
from User import User

from utils import ask_in_range, console, ask_string


class Administrator(Session):
    def output_inventory(self):
        print(
            f"\n[yellow]Inventario de {self.current.user.get_name()} ({self.current.user.get_id()})[/]\n"
        )
        for equipment in self.current.saved_equipment:
            print(f"* {equipment}")

    def add_equipment(self):
        print()
        print("[green]Ingrese los datos solicitados[/]")

        equipment = Equipment.ask()

        item = InventoryItem(
            username=self.current.user.get_name(),
            user_id=self.current.user.get_id(),
            name=equipment.get_name(),
            serial_number=equipment.get_serial_number(),
            purchase_date=equipment.get_purchase_date(),
            price=equipment.get_price(),
        )

        saved_inventory = self.shared.saved_inventory
        deleted_inventory = self.shared.deleted_inventory

        saved_item_node = saved_inventory.find_if(
            lambda saved_item: (
                saved_item.get_equipment().get_serial_number() == item.get_serial_number()
                and saved_item.get_user_id() == item.get_user_id()
            )
        )

        if saved_item := saved_item_node is not None:
            saved_item = saved_item_node.get_data()
            console.print(f"[yellow]\nEl quipo con el número serial {item.get_serial_number()} ya se encuentra en el inventario[/]")
            console.print(saved_item.to_csv())
            return

        deleted_item_node = deleted_inventory.find_if(
            lambda deleted_item: (
                deleted_item.get_equipment() == equipment
                and deleted_item.get_user_id() == self.current.user.get_id()
            )
        )

        if deleted_item_node is not None:
            deleted_item = deleted_item_node.get_data()
            deleted_inventory.erase(
                deleted_inventory.find_if(
                    lambda item: item == deleted_item
                )
            )

            deleted_inventory.save_to_file()

            console.print("[green]\nSe ha transferido el equipo del inventario eliminado al inventario general[/]")
            console.print(deleted_item.to_csv())


        saved_inventory.push_back(item)
        saved_inventory.sorted(key=lambda item: item.get_serial_number()).save_to_file()

        if deleted_item_node is None:
            print("[green]\nSe ha guardado el equipo")

    def delete_equipment(self):
        current_saved_inventory = self.current.saved_inventory

        shared_saved_inventory = self.shared.saved_inventory
        shared_deleted_inventory = self.shared.deleted_inventory

        print()
        indexes = EquipmentList(
            current_saved_inventory.apply(lambda item: item.get_equipment())
        ).choose()
        selected_items = tuple(current_saved_inventory[index] for index in indexes)

        for selected_item in selected_items:
            shared_saved_inventory.erase(
                shared_saved_inventory.find_if(
                    lambda saved_item: saved_item == selected_item
                )
            )

        shared_saved_inventory.save_to_file()

        shared_deleted_inventory.extend(selected_items)
        shared_deleted_inventory.sorted(
            key=lambda item: item.get_serial_number()
        ).save_to_file()

        print("[red]\nSe ha eliminado el equipo[/]")
        for item in selected_items:
            print(item.get_equipment())

    def add_user(self):
        print()
        print("[green]Ingrese los datos del usuario[/]")

        credentials = Credentials.ask()
        print()
        user = User.ask()

        credentials_list = self.shared.credentials_list
        users = self.shared.users

        credentials_list.push_back(credentials)
        users.push_back(user)

        credentials_list.save_to_file()
        users.save_to_file()

    def delete_user(self):
        credentials_list = self.shared.credentials_list
        users = self.shared.users

        print()
        indexes = credentials_list.choose()
        selected_credentials = tuple(credentials_list[index] for index in indexes)
        selected_user_ids = tuple(
            credentials.get_user_id() for credentials in selected_credentials
        )

        credentials_list.filter_if(
            lambda credentials: credentials not in selected_credentials
        ).save_to_file()

        users.filter_if(
            lambda user: user.get_id() not in selected_user_ids
        ).save_to_file()

    def change_user_password(self):
        credentials_list = self.shared.credentials_list

        print()
        indexes = credentials_list.choose()

        for index in indexes:
            current_credentials = credentials_list[index]
            current_user = current_credentials.get_user()

            print(f"\n{current_user.get_name()} {current_user.get_id()}")
            password = ask_string("Ingrese una nueva contraseña: ")

            credentials_list.find_if(
                lambda credentials: credentials.get_user_id()
                == current_credentials.get_user_id()
            ).get_data().set_password(password)

        credentials_list.save_to_file()

    def manage_requests(self):
        pending_requests = self.shared.pending_requests

        indexes = pending_requests.choose()

        selected_pending_requests = tuple(pending_requests[index] for index in indexes)

        for pending_request in selected_pending_requests:
            print(f"\n{pending_request}\n")
            print("1. [green]Aprobar Solicitud[/]")
            print("2. [red]Rechazar Solicitud[/]")
            print("3. Siguiente Solicitud\n")

            choice = ("aprobar", "rechazar", "siguiente")[
                ask_in_range(
                    range_=range(1, 4),
                    variadic=False,
                    prompt="Seleccione una opción: ",
                    error_message="Entrada no válida. Asegúrese de ingresar un número válido correspondiente a una de las opciones.",
                )
                - 1
            ]

            if choice == "siguiente":
                continue

            elif choice == "aprobar":
                pending_request.approve(self)

            elif choice == "rechazar":
                pending_request.reject(self)

    def save_user_inventory(self):
        credentials_list = self.shared.credentials_list
        inventory = self.shared.inventory

        print()
        indexes = credentials_list.choose()

        for index in indexes:
            current_credentials = credentials_list[index]
            current_user = current_credentials.get_user()

            EquipmentList(
                inventory.filter_if(
                    lambda item: item.get_user_id() == current_credentials.get_user_id()
                ).apply(lambda item: item.get_equipment())
            ).save_to_file(
                filename=f"{current_user.get_name()} {current_user.get_id()}.txt"
            )

    def output_changelog(self):
        print("\nControl de cambios")
        print(f"{self.shared.changelog}")

    def display_menu(self):
        options = [
            ("Consultar equipo en inventario", self.output_inventory),
            ("Agregar equipo", self.add_equipment),
            ("Eliminar equipo", self.delete_equipment),
            ("Registrar usuario", self.add_user),
            ("Eliminar usuario", self.delete_user),
            ("Cambiar contraseña de un usuario", self.change_user_password),
            ("Administrar solicitudes", self.manage_requests),
            (
                "Generar información de inventario de un usuario",
                self.save_user_inventory,
            ),
            ("Consultar control de cambios", self.output_changelog),
        ]

        console.rule(
            f"[yellow]{self.current.user.get_name()} ({self.current.user.get_id()})[/] [blue]\[rol: {self.current.credentials.get_role()}][/]"
        )
        print()
        for index, option in enumerate(options, start=1):
            option_message, _ = option

            print(f"{index}. {option_message}")
        print()

        choice = ask_in_range(
            range_=range(1, len(options) + 1),
            variadic=False,
            prompt="Seleccione una opción: ",
            error_message=f"Por favor ingrese un número entre 1 y {len(options)}",
        )

        options[choice - 1][1]()
        input("\n")
