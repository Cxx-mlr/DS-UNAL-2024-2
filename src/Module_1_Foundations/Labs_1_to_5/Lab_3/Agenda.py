from __future__ import annotations

from User import User

from typing import List, Optional
from pathlib import Path

class Agenda:
    def __init__(self, capacity: int) -> Agenda:
        self.__capacity: int = capacity

        self.__user_list: List[Optional[User]] = [None for _ in range(self.__capacity)]
        self.__registered_count: int = 0

    def add_user(self, user: User) -> bool:
        if self.__registered_count >= self.__capacity:
            return False
        
        if self.find_user(user.get_id()) != -1:
            return False
        
        for index, registered_user in enumerate(self.__user_list):
            if registered_user is None:
                self.__user_list[index] = user
                break

        self.__registered_count += 1
        return True

    def find_user(self, user_id: int) -> int:
        for index, user in enumerate(self.__user_list):
            if user is None:
                break
            if user.get_id() == user_id:
                return index
        return -1

    def delete_user(self, user_id: int) -> bool:
        index = self.find_user(user_id)
        if index == -1:
            return False
        

        self.__user_list[index] = None
        for next_index in range(index + 1, self.__capacity):
            self.__user_list[index] = self.__user_list[next_index]
            self.__user_list[next_index] = None
        
        self.__registered_count -= 1
        return True

    def save_to_file(self, filename: str = "agenda.txt"):
        data = [registered_user.to_csv() for registered_user in self.__user_list[:self.__registered_count]]
        with open(Path(__file__).parent / filename, "wt", encoding="utf-8") as file:
            file.writelines(
                data
            )

    def load_from_file(self, filename: str = "agenda.txt"):
        try:
            with open(Path(__file__).parent / filename, "rt", encoding="utf-8") as file:
                for csv_string in file:
                    user = User.from_csv(csv_string=csv_string.strip())
                    self.add_user(user)
        except FileNotFoundError:
            print("File not found. Failed to load data.")

    def __repr__(self) -> str:
        return (
            f"Agenda("
            f"capacity={self.__capacity!r}, "
            f"registered_count={self.__registered_count!r}, "
            f"users={self.__user_list!r}"
            f")"
        )

    def __str__(self) -> str:
        users_str = "".join([f"\n{user!s}\n" for user in self.__user_list[:self.__registered_count]])
        return (
            f"[green]Agenda Capacity:[/] {self.__capacity}" \
            f"\n[green]Number of Registered Users:[/] {self.__registered_count}" \
            f"\n\n[green]Users:[/]\n{users_str}"
        )