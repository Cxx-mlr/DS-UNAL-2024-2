from typing_extensions import Optional, Union

from config import PASSWORDS_PATH, EMPLOYEES_PATH
from utils import ask_integer, ask_string

from UserList import UserList
from CredentialsList import CredentialsList
from Researcher import Researcher
from Administrator import Administrator


def authenticate(
    user_list: UserList, user_id: int, password: str
) -> Optional[Union[Researcher, Administrator]]:
    with CredentialsList(filename=PASSWORDS_PATH) as credentials_list:
        credentials_node = credentials_list.find_if(
            lambda credentials: credentials.get_user_id() == user_id
        )

    if credentials_node is None:
        return None
    else:
        credentials = credentials_node.get_data()

    if not credentials.get_password() == password:
        return None

    user_node = user_list.find_if(lambda user: user.get_id() == credentials.get_user_id())

    if user_node is None:
        return None

    else:
        user = user_node.get_data()

    if credentials.is_researcher():
        return Researcher(user)

    elif credentials.is_administrator():
        return Administrator(user)


def login(
    user_id: Optional[int] = None, password: Optional[str] = None
) -> Optional[Union[Researcher, Administrator]]:
    user_list = UserList(capacity=13)
    user_list.load_from_file(filename=EMPLOYEES_PATH)

    if user_id is None:
        user_id = ask_integer("ID: ", "Por favor, proporcione un ID de usuario válido.")
    if password is None:
        password = ask_string("Contraseña: ")

    session = authenticate(user_list, user_id, password)

    if not session:
        print("Usuario o contraseña incorrectos.")
        exit()

    return session