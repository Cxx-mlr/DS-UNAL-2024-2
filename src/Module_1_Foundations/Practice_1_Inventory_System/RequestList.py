from Request import Request
from FileBackedList import FileBackedList

from typing_extensions import Set, Literal


class RequestList(FileBackedList[Request]):
    T = Request

    def choose(self) -> Set[int]:
        return super().choose(
            rule="Seleccione una o varias solicitudes",
            prompt="Ingrese uno o varios números separados por espacio: ",
            error_message="Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones.",
        )

    def set_action(self, action: Literal["agregar", "eliminar"]):
        self.for_each(lambda request: request.set_action(action))

    def set_status(self, status: Literal["PENDING", "APPROVED", "REJECTED"]):
        self.for_each(lambda request: request.set_status(status))
