from __future__ import annotations

from typing_extensions import Set
from Equipment import Equipment

from FileBackedList import FileBackedList


class EquipmentList(FileBackedList[Equipment]):
    T = Equipment

    def choose(self) -> Set[int]:
        return super().choose(
            rule="Seleccione uno o varios equipos",
            prompt="Ingrese uno o varios números separados por espacio: ",
            error_message="Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones.",
            lambda_repr=lambda item: item.to_csv(),
        )
