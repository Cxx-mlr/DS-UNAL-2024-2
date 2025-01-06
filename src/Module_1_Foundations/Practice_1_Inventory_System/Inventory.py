from __future__ import annotations
from rich import print

from typing_extensions import Optional, Literal, List, Callable, TYPE_CHECKING

from utils import console, ask_in_range
from config import WRITE_PATH, READ_PATH
from InventoryItem import InventoryItem

if TYPE_CHECKING:
    from Session import Session

class Inventory:
    def __init__(self, capacity: int = 100) -> Inventory:
        self.__capacity: int = capacity

        self.__items_list: List[Optional[InventoryItem]] = [None for _ in range(self.__capacity)]
        self.__items_count: int = 0

    def choose(self, session: "Session", *, rule: str = "", request: bool = False, what: Literal["agregar", "eliminar"] = "") -> List[int]:
        console.rule(rule)

        for i, item in enumerate(self, start=1):
            if request:
                equipment = item.get_equipment()
                what_repr = f"[green]{what.capitalize()}[/]" if what == "agregar" else f"[red]{what.capitalize()}[/]"
                request_repr = (
                    f"[cyan]Solicitud de [yellow]{item.get_username()} {item.get_user_id()}[/]"
                    f"\n   - {what_repr} equipo {equipment.get_name()} {equipment.get_serial_number()}[/] [[green]${equipment.get_price()}[/]]"
                )
                print(f"{i}. {request_repr}")
                print()
            else:
                print(f"{i}. {item.get_equipment()}")

        if not request: print()
        choices = ask_in_range(
            range(1, self.__items_count + 1),
            True,
            "Ingrese uno o varios números separados por espacio: ",
            "Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones."
        )

        return [choice - 1 for choice in choices]

    def add(self, item: InventoryItem) -> Optional[InventoryItem]:
        if self.__items_count >= self.__capacity:
            return None
        
        for index, item_i in enumerate(self.__items_list):
            if item_i is None:
                self.__items_list[index] = item
                break

        self.__items_count += 1
        return item

    def delete(self, pred: Callable[[InventoryItem], bool]) -> Optional[InventoryItem]:
        if (index := self.index(pred)) == -1:
            return None

        deleted = self.__items_list[index]
        self.__items_list[index] = None
        for next_index in range(index + 1, self.__capacity):
            self.__items_list[next_index - 1] = self.__items_list[next_index]
            self.__items_list[next_index] = None
        
        self.__items_count -= 1
        return deleted

    def find(self, pred: Callable[[InventoryItem], bool]) -> Optional[Inventory]:
        for item in self:
            if pred(item):
                return item
        return None
    
    def index(self, pred: Callable[[InventoryItem], bool]) -> int:
        for index, item in enumerate(self):
            if pred(item):
                return index
        return -1
    
    def filter(self, pred: Callable[[InventoryItem], bool]) -> Inventory:
        new_inventory = Inventory()

        for item in self:
            if pred(item):
                new_inventory.add(item)
        
        return new_inventory
    
    def sort(self, reverse: bool = False) -> Inventory:
        comp = (lambda lhd, rhd: lhd > rhd) if not reverse else (lambda lhd, rhd: lhd < rhd)

        for i in range(1, self.__items_count):
            j = i - 1
            current_value = self.__items_list[i]
            while j >= 0 and comp(self.__items_list[j].get_serial_number(), current_value.get_serial_number()):
                self.__items_list[j + 1] = self.__items_list[j]
                j -= 1
            self.__items_list[j + 1] = current_value

        return self

    def __getitem__(self, index: int) -> InventoryItem:
        return self.__items_list[:self.__items_count][index]
    
    def __iter__(self):
        return iter(
            self.__items_list[:self.__items_count]
        )
    
    def __enter__(self) -> Inventory:
        return self
    
    def __exit__(self, type, value, traceback):
        return False

    def save_to_file(self, filename: str = "InventarioGeneral.txt", *, only_equipment: bool = False):
        data = "\n".join(
            (item.get_equipment() if only_equipment else item).to_csv()
            for item in self
        )
        with open(WRITE_PATH / filename, "wt", encoding="utf-8") as file:
            file.writelines(
                data
            )

    def load_from_file(self, filename: str = "InventarioGeneral.txt"):
        try:
            with open(READ_PATH / filename, "rt", encoding="utf-8") as file:
                for csv_string in file:
                    item = InventoryItem.from_csv(csv_string)
                    self.add(item)
        except FileNotFoundError:
            print("File not found. Failed to load data.")

    def __str__(self) -> str:
        return "\n".join(f"{item}" for item in self)