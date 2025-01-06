from __future__ import annotations

from rich import print

from typing_extensions import Literal

from utils import console, ask_integer
from contextlib import suppress

from Role import Role

class Credentials:
    def __init__(self, user_id: int, password: str, role: str = Literal["investigador", "administrador"]):
        assert role in ("investigador", "administrador"), "Role must be either 'investigador' or 'administrador'"
        self.__user_id = user_id
        self.__password = password
        self.__role = role

    @classmethod
    def ask(cls) -> Credentials:
        console.rule("Credenciales")
        user_id = ask_integer("ID: ", "Por favor, proporcione un ID de usuario válido.")
        print("[blue]Contraseña: [/]", end="", flush=True)
        password = input("")

        role = Role.ask()

        return cls(
            user_id=user_id,
            password=password,
            role=role
        )

    def get_user_id(self) -> int:
        return self.__user_id
    
    def get_password(self) -> str:
        return self.__password
    
    def get_role(self) -> Literal["investigador", "administrador"]:
        return self.__role
    
    def set_password(self, new_password: str):
        self.__password = new_password
    
    def is_researcher(self) -> bool:
        return self.__role == "investigador"
    
    def is_administrator(self) -> bool:
        return self.__role == "administrador"

    def to_csv(self) -> str:
        return f"{self.__user_id} {self.__password} {self.__role}"
    
    @staticmethod
    def from_csv(csv_string: str) -> Credentials:
        user_id, password, role = csv_string.strip().split(" ")
        user_id = int(user_id)

        return Credentials(
            user_id=user_id,
            password=password,
            role=role
        )
    
    def __str__(self) -> str:
        return self.to_csv()