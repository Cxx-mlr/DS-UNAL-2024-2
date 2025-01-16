from User import User
from FileBackedList import FileBackedList

from typing_extensions import List


class UserList(FileBackedList[User]):
    T = User

    def choose(self) -> List[int]:
        return super().choose(
            rule="Seleccione uno o varios usuarios",
            prompt="Ingrese uno o varios números separados por espacio: ",
            error_message="Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones.",
            lambda_repr=lambda item: item.to_csv(),
        )
