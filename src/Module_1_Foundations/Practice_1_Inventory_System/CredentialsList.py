from __future__ import annotations
from rich import print

from utils import console, ask_in_range

from typing_extensions import List, Optional, Callable, TYPE_CHECKING

from config import WRITE_PATH, READ_PATH
from Credentials import Credentials

if TYPE_CHECKING:
    from Session import Session

class CredentialsList:
    def __init__(self, capacity: int = 100):
        self.__capacity: int = capacity

        self.__credentials_list: List[Optional[Credentials]] = [None for _ in range(self.__capacity)]
        self.__credentials_count: int = 0

    def choose(self, session: "Session") -> List[index]:
        console.rule("Seleccione uno o varios usuarios")

        for i, credentials in enumerate(self, start=1):
            user = session._users.find(
                lambda user: user.get_id() == credentials.get_user_id()
            )

            print(f"{i}. {user.get_name()} {user.get_id()}")

        print()
        choices = ask_in_range(
            range(1, self.__credentials_count + 1),
            True,
            "Ingrese uno o varios números separados por espacio: ",
            "Entrada no válida. Asegúrese de ingresar números válidos correspondientes a las opciones."
        )

        return [choice - 1 for choice in choices]

    def __enter__(self) -> CredentialsList:
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def add(self, credentials: Credentials) -> Optional[Credentials]:
        if self.__credentials_count >= self.__capacity:
            return None
        
        for index, registered_user in enumerate(self.__credentials_list):
            if registered_user is None:
                self.__credentials_list[index] = credentials
                break

        self.__credentials_count += 1
        return credentials

    def delete(self, pred: Callable[[Credentials], bool]) -> Optional[Credentials]:
        if (index := self.index(pred)) == -1:
            return None

        deleted = self.__credentials_list[index]
        self.__credentials_list[index] = None
        for next_index in range(index + 1, self.__credentials_count):
            self.__credentials_list[next_index - 1] = self.__credentials_list[next_index]
            self.__credentials_list[next_index] = None
        
        self.__credentials_count -= 1
        return deleted
    
    def find(self, pred: Callable[[Credentials], bool]) -> Optional[Credentials]:
        for credentials in self:
            if pred(credentials):
                return credentials
        return None
    
    def index(self, pred: Callable[[Credentials], bool]) -> Optional[Credentials]:
        for index, credentials in enumerate(self):
            if pred(credentials):
                return index
        return -1
    
    def filter(self, pred: Callable[[Credentials], bool]) -> CredentialsList:
        new_credentials = CredentialsList()

        for credentials in self:
            if pred(credentials):
                new_credentials.add(credentials)

        return new_credentials
    
    def __getitem__(self, index: int) -> Credentials:
        return self.__credentials_list[:self.__credentials_count][index]
    
    def __iter__(self):
        return iter(self.__credentials_list[:self.__credentials_count])

    def load_from_file(self, filename: str = "Password.txt"):
        try:
            with open(READ_PATH / filename, "rt", encoding="utf-8") as file:
                for csv_string in file:
                    credentials = Credentials.from_csv(csv_string=csv_string)
                    self.add(credentials)
        except FileNotFoundError:
            print("File not found. Failed to load data.")

    def save_to_file(self, filename: str = "Password.txt"):
        data = "\n".join(
            credentials.to_csv()
            for credentials in self
        )
        with open(WRITE_PATH / filename, "wt", encoding="utf-8") as file:
            file.writelines(
                data
            )

    def __str__(self):
        return "\n".join(f"{credentials}" for credentials in self)