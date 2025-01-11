from __future__ import annotations

from typing_extensions import Set

from InventoryItem import InventoryItem
from FileBackedList import FileBackedList


class Inventory(FileBackedList[InventoryItem]):
    T = InventoryItem

    def choose(self) -> Set[int]:
        return super().choose(
            rule="Seleccione uno o varios equipos",
            prompt="Ingrese uno o varios números separados por espacio: ",
            error_message="Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones.",
        )
