from __future__ import annotations
from rich import print

from typing_extensions import Optional, Union

from Agenda import Agenda
from CredentialsList import CredentialsList
from Researcher import Researcher
from Administrator import Administrator


def authenticate(agenda: Agenda, user_id: int, password: str) -> Optional[Union[Researcher, Administrator]]:
    credentials_list = CredentialsList()
    credentials_list.load_from_file(filename="Password.txt")

    credentials = credentials_list.find(
        lambda l_credentials: l_credentials.get_user_id() == user_id
    )

    if not credentials:
        return None

    if not credentials.get_password() == password:
        return None

    user = agenda.find(
        lambda user: user.get_id() == credentials.get_user_id()
    )

    if not user:
        return None

    if credentials.is_researcher():
        return Researcher(user)
    elif credentials.is_administrator():
        return Administrator(user)

def main():
    agenda = Agenda(capacity=13)
    agenda.load_from_file(filename="Empleados.txt")

    # researcher
    # cc = 24567898
    # password = "j4an1980$"

    # administrator
    user_id = 2345902
    password = "c4100l485Cal$"

    session = authenticate(agenda, user_id, password)

    if not session:
        print("Usuario o contraseña incorrectos")
        exit()

    session.display_menu()

if __name__ == "__main__":
    main()