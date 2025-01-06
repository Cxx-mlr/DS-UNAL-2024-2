from __future__ import annotations

from typing_extensions import List, Optional, Callable

from config import WRITE_PATH, READ_PATH
from User import User

class Agenda:
    def __init__(self, capacity: int = 100) -> Agenda:
        self.__capacity: int = capacity

        self.__user_list: List[Optional[User]] = [None for _ in range(self.__capacity)]
        self.__user_count: int = 0

    def __enter__(self) -> Agenda:
        return self
    
    def __exit__(self, type, value, traceback) -> Agenda:
        pass

    def add(self, user: User) -> Optional[User]:
        if self.__user_count >= self.__capacity:
            return False
        
        if self.find(
            lambda l_user: l_user.get_id() == user.get_id()
        ):
            return None
        
        for index, registered_user in enumerate(self.__user_list):
            if registered_user is None:
                self.__user_list[index] = user
                break

        self.__user_count += 1
        return user

    def delete(self, pred: Callable[[User], bool]) -> Optional[User]:
        if (index := self.index(pred)) == -1:
            return None

        deleted = self.__user_list[index]
        self.__user_list[index] = None
        for next_index in range(index + 1, self.__capacity):
            self.__user_list[next_index - 1] = self.__user_list[next_index]
            self.__user_list[next_index] = None
        
        self.__user_count -= 1
        return deleted
    
    def find(self, pred: Callable[[User], bool]) -> Optional[User]:
        for user in self.__user_list[:self.__user_count]:
            if pred(user):
                return user
        return None
    
    def index(self, pred: Callable[[User], bool]) -> int:
        for index, user in enumerate(self.__user_list[:self.__user_count]):
            if pred(user):
                return index
        return -1
    
    def filter(self, pred: Callable[[User], bool]) -> Agenda:
        new_agenda = Agenda()

        for user in self.__user_list[:self.__user_count]:
            if pred(user):
                new_agenda.add(user)
        
        return new_agenda
    
    def __getitem__(self, index: int) -> User:
        return self.__user_list[:self.__user_count][index]
    
    def __iter__(self):
        return iter(self.__user_list[:self.__user_count])

    def save_to_file(self, filename: str = "Empleados.txt"):
        data = "\n".join(
            user.to_csv() for user in self
        )
        with open(WRITE_PATH / filename, "wt", encoding="utf-8") as file:
            file.writelines(
                data
            )

    def load_from_file(self, filename: str = "Empleados.txt"):
        try:
            with open(READ_PATH / filename, "rt", encoding="utf-8") as file:
                for csv_string in file:
                    user = User.from_csv(csv_string=csv_string.strip())
                    self.add(user)
        except FileNotFoundError:
            print("File not found. Failed to load data.")

    def __repr__(self) -> str:
        return (
            f"Agenda("
            f"capacity={self.__capacity!r}, "
            f"registered_count={self.__user_count!r}, "
            f"users={self.__user_list!r}"
            f")"
        )

    def __str__(self) -> str:
        users_str = "".join([f"\n{user!s}\n" for user in self.__user_list[:self.__user_count]])
        return (
            f"[green]Agenda Capacity:[/] {self.__capacity}" \
            f"\n[green]Number of Registered Users:[/] {self.__user_count}" \
            f"\n\n[green]Users:[/]\n{users_str}"
        )