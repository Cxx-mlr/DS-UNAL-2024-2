from __future__ import annotations
from rich import print

from typing_extensions import Union, TextIO
from io import StringIO
import sys

from config import REQUESTS_STATUS_FILENAME, DATA_PATH
from utils import console, ask_in_range

from Equipment import Equipment
from Request import Request
from Session import Session


class Researcher(Session):
    def output_inventory(self):
        print(
            f"\n[yellow]Inventario de {self.current.user.get_name()} ({self.current.user.get_id()})[/]\n"
        )
        for equipment in self.current.saved_equipment:
            print(f"* {equipment}")

    def add_equipment(self):
        print("\n[green]Ingrese los datos solicitados[/]")

        equipment = Equipment.ask()

        request = Request(
            username=self.current.user.get_name(),
            user_id=self.current.user.get_id(),
            name=equipment.get_name(),
            serial_number=equipment.get_serial_number(),
            purchase_date=equipment.get_purchase_date(),
            price=equipment.get_price(),
        )

        request.set_action("agregar")
        request.set_status("PENDING")
        request.submit()

    def delete_equipment(self):
        print("\n[green]Ingrese los datos solicitados[/]")

        equipment = Equipment.ask()

        request = Request(
            username=self.current.user.get_name(),
            user_id=self.current.user.get_id(),
            name=equipment.get_name(),
            serial_number=equipment.get_serial_number(),
            purchase_date=equipment.get_purchase_date(),
            price=equipment.get_price(),
        )

        request.set_action("eliminar")
        request.set_status("PENDING")
        request.submit()

    def output_requests_status(self, file: Union[StringIO, TextIO] = sys.stdout):
        pending_requests = self.current.pending_requests
        approved_requests = self.current.approved_requests
        rejected_requests = self.current.rejected_requests

        print(
            f"PENDIENTES: {pending_requests.size():<10} APROBADAS: {approved_requests.size():<10} RECHAZADAS: {rejected_requests.size()}",
            file=file,
        )

        if not pending_requests.empty():
            print("\nPENDIENTES", file=file)
            print(f"{pending_requests}", file=file)

        if not approved_requests.empty():
            print("\nAPROBADAS", file=file)
            print(f"{approved_requests}", file=file)

        if not rejected_requests.empty():
            print("\nRECHAZADAS", file=file)
            print(f"{rejected_requests}", file=file)

        if isinstance(file, StringIO):
            save_path = DATA_PATH / REQUESTS_STATUS_FILENAME.format(
                self.current.user.get_name(), self.current.user.get_id()
            )
            with open(save_path, "wt", encoding="utf-8") as fp:
                fp.write(file.getvalue().strip())

            print(f"\nSe ha generado el archivo [yellow]'{save_path.name}'[/]")

    def save_requests_status(self):
        return self.output_requests_status(file=StringIO())

    def save_inventory(self):
        equipment = self.current.saved_equipment
        equipment.sorted(lambda equipment: equipment.get_serial_number()).save_to_file(
            filename=f"{self.current.user.get_name()} {self.current.user.get_id()}.txt"
        )

    def display_menu(self):
        options = [
            ("Consultar equipo en inventario", self.output_inventory),
            ("Solicitar adición de equipo", self.add_equipment),
            ("Solicitar eliminación de equipo", self.delete_equipment),
            ("Consultar estado de solicitudes", self.output_requests_status),
            ("Generar archivo con información de inventario", self.save_inventory),
            ("Generar archivo con estado de solicitudes", self.save_requests_status),
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
