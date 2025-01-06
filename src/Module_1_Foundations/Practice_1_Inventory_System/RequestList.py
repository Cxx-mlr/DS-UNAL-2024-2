from __future__ import annotations
from rich import print

from typing_extensions import Literal, List, TYPE_CHECKING

from utils import console, ask_in_range, ask_integer

from Inventory import Inventory

if TYPE_CHECKING:
    from Session import Session

class RequestList(Inventory):
    def choose(self, session: "Session", *, rule: str = "", what: str = "") -> List[int]:
        console.rule(rule)

        for i, item in enumerate(self, start=1):
            equipment = item.get_equipment()
            what_repr = f"[green]{what.capitalize()}[/]" if what == "agregar" else f"[red]{what.capitalize()}[/]"
            request_repr = (
                f"[cyan]Solicitud de [yellow]{item.get_username()} {item.get_user_id()}[/]"
                f"\n   - {what_repr} equipo {equipment.get_name()} {equipment.get_serial_number()}[/] [[green]${equipment.get_price()}[/]]"
            )
            print(f"{i}. {request_repr}")
            print()

        choices = ask_in_range(
            range(1, self.__items_count + 1),
            True,
            "Ingrese uno o varios números separados por espacio: ",
            "Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones."
        )

        return [choice - 1 for choice in choices]

    def get_what(self) -> str:
        return self.__what