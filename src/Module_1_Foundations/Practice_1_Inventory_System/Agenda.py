from User import User
from FileBackedList import FileBackedList

from typing_extensions import List


class Agenda(FileBackedList[User]):
    T = User

    def choose(self) -> List[int]:
        return super().choose(
            rule="Seleccione uno o varios usuarios",
            input_message="Ingrese uno o varios números separados por espacio: ",
            fail_message="Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones.",
            lambda_repr=lambda item: item.to_csv(),
        )
