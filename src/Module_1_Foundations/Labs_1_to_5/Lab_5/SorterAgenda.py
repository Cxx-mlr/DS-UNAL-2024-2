from __future__ import annotations

from rich import print

from typing_extensions import Self
from DoubleList import DoubleList
from User import User


class SorterAgenda:
    def __init__(self) -> Self:
        self.__double_list: DoubleList[User] = DoubleList[User]()

    def add_user(self, user: User) -> None:
        self.__double_list.push_back(user)

    def sort(self) -> None:
        for _ in range(self.__double_list.size()):
            current = self.__double_list.begin()
            while current and current.get_next():
                next_node = current.get_next()
                if current.get_data().get_id() > next_node.get_data().get_id():
                    current_data = current.get_data()
                    current.set_data(next_node.get_data())
                    next_node.set_data(current_data)
                current = next_node

    def __str__(self) -> str:
        return f"{self.__double_list}"

    def display(self):
        current_node = self.__double_list.begin()
        while current_node:
            user = current_node.get_data()
            print(
                f"[yellow bold]Nombre:[/] {user.get_name()} | "
                f"[yellow bold]ID:[/] {user.get_id()} | "
                # f"[yellow bold]Fecha de nacimiento:[/] {user.get_birth_date()} | "
                # f"[yellow bold]Ciudad de nacimiento:[/] {user.get_birth_city()} | "
                # f"[yellow bold]Teléfono:[/] {user.get_phone_number()} | "
                # f"[yellow bold]Email:[/] {user.get_email()} | "
                # f"[yellow bold]Dirección:[/] {user.get_address()}"
            )
            current_node = current_node.get_next()
