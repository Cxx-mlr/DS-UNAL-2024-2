from __future__ import annotations
from rich import print

from utils import console, ask_in_range

from typing_extensions import (
    Set,
    Optional,
    Callable,
    TYPE_CHECKING,
    overload,
    Iterable,
    Self,
)

from config import DATA_PATH

if TYPE_CHECKING:
    from Session import Session

from DoubleList import DoubleList

from Protocols import T


class FileBackedList(DoubleList[T]):
    T: T

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, session: Session) -> None: ...

    @overload
    def __init__(self, filename: str) -> None: ...

    @overload
    def __init__(self, session: Session, filename: str) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[T], /) -> None: ...

    @overload
    def __init__(self, double_list: DoubleList[T], /) -> None: ...

    @overload
    def __init__(self, iterable: FileBackedList[T], /) -> None: ...

    def __init__(self, arg=None, **kwargs):
        if isinstance(arg, FileBackedList):
            self.__session = arg.get_session()
            self.__filename = arg.get_filename()
        else:
            self.__session = None
            self.__filename = None

        self.__session: Optional[Session] = kwargs.get("session", self.__session)
        self.__filename: Optional[str] = kwargs.get("filename", self.__filename)

        super().__init__(arg)

    def get_session(self):
        return self.__session

    def get_filename(self):
        return self.__filename

    def choose(
        self,
        rule: str,
        prompt: str,
        error_message: str,
        lambda_repr: Optional[Callable[[T], bool]] = None,
    ) -> Set[int]:
        console.rule(rule)

        for index, item in enumerate(self, start=1):
            print(f"{index}. {lambda_repr(item) if lambda_repr else item}")

        print()
        choices = ask_in_range(range(1, self.size() + 1), True, prompt, error_message)

        return set(choice - 1 for choice in choices)

    def __enter__(self):
        self.load_from_file()
        return self

    def __exit__(self, type, value, traceback):
        return False

    def clone(self) -> Self[T]:
        return self.__class__(self)

    def loose_clone(self) -> Self[T]:
        return self.__class__(filename=self.get_filename(), session=self.get_session())

    def filter(self, data: T) -> Self[T]:
        items: DoubleList[T] = super().filter(data)
        filtered_list = self.__class__(
            filename=self.get_filename(), session=self.get_session()
        )
        filtered_list.extend(items)

        return filtered_list

    def filter_if(self, pred: Callable[[T], bool]) -> Self[T]:
        items: DoubleList[T] = super().filter_if(pred)
        filtered_list = self.__class__(
            filename=self.get_filename(), session=self.get_session()
        )
        filtered_list.extend(items)

        return filtered_list

    def load_from_file(self, filename: Optional[str] = None):
        filename = filename or self.get_filename()
        try:
            with open(DATA_PATH / filename, "rt", encoding="utf-8") as file:
                for csv_string in file:
                    items = self.__class__.T.from_csv(csv_string=csv_string)
                    self.push_back(items)
        except FileNotFoundError:
            print(f"{filename}: File not found. Failed to load data.")

    def save_to_file(self, filename: Optional[str] = None):
        filename = filename or self.get_filename()
        data = "\n".join(items.to_csv() for items in self)
        try:
            with open(DATA_PATH / filename, "wt", encoding="utf-8") as file:
                file.writelines(data)
        except FileNotFoundError:
            print(f"{filename}: File not found. Failed to load data.")

    def __str__(self) -> str:
        return "\n".join(f"{items}" for items in self)
