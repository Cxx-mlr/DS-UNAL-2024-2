from Credentials import Credentials
from FileBackedList import FileBackedList

from typing_extensions import Set


class CredentialsList(FileBackedList[Credentials]):
    T = Credentials

    def choose(self) -> Set[int]:
        return super().choose(
            rule="Seleccione uno o varios usuarios",
            prompt="Ingrese uno o varios números separados por espacio: ",
            error_message="Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones.",
        )
