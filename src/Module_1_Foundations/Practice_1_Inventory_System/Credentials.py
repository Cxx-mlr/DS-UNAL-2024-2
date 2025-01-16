from __future__ import annotations

from rich import print

from typing_extensions import Literal, Optional

from utils import console, ask_integer
from config import EMPLOYEES_PATH
from User import User

from Role import Role


class Credentials:
    def __init__(
        self,
        user_id: Optional[int] = None,
        password: Optional[str] = None,
        role: Optional[Literal["investigador", "administrador"]] = None,
    ):
        assert role is None or role in (
            "investigador",
            "administrador",
        ), "Role must be either 'investigador' or 'administrador'"
        self.__user_id = user_id
        self.__password = password
        self.__role = role

    @classmethod
    def ask(cls) -> Credentials:
        console.rule("Credenciales")
        user_id = ask_integer("ID: ", "Por favor, proporcione un ID de usuario válido.")
        print("[blue]Contraseña: [/]", end="", flush=True)
        password = input("")

        print()
        role = Role.ask()

        return cls(user_id=user_id, password=password, role=role)

    def get_user(self) -> User:
        from UserList import UserList

        with UserList(filename=EMPLOYEES_PATH) as users:
            node = users.find_if(lambda user: user.get_id() == self.get_user_id())

            if node is None:
                return User(id=self.get_user_id())

            return node.get_data()

    def get_user_id(self) -> Optional[int]:
        return self.__user_id

    def get_password(self) -> Optional[str]:
        return self.__password

    def get_role(self) -> Optional[Literal["investigador", "administrador"]]:
        return self.__role

    def set_role(self, role: Literal["investigador", "administrador"]):
        self.__role = role

    def set_password(self, password: str):
        self.__password = password

    def is_researcher(self) -> bool:
        return self.__role == "investigador"

    def is_administrator(self) -> bool:
        return self.__role == "administrador"

    def to_csv(self) -> str:
        return f"{self.__user_id} {self.__password} {self.__role}"

    @staticmethod
    def from_csv(csv_string: str) -> Credentials:
        parts = csv_string.strip().split()

        if len(parts) != 3:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 3 partes separadas por espacios, pero tiene {len(parts)} partes: {parts}"
            )

        try:
            user_id = int(parts[0]) if parts[0] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'user_id' a un entero. Valor proporcionado: {parts[0]}"
            )
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'user_id' de la cadena CSV. Partes: {parts}"
            )

        try:
            password = parts[1]
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'password' de la cadena CSV. Partes: {parts}"
            )

        try:
            role = parts[2]
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'role' de la cadena CSV. Partes: {parts}"
            )

        if role is not None and role not in ("investigador", "administrador"):
            raise ValueError(
                f"Rol inválido '{role}' en la cadena CSV: {csv_string}. El rol debe ser 'investigador' o 'administrador'."
            )

        return Credentials(user_id=user_id, password=password, role=role)

    def __str__(self) -> str:
        user = self.get_user()
        return f"{user.get_name()} {user.get_id()} {self.get_role()}"
