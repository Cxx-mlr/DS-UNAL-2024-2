from typing_extensions import Generic, TypeVar

T = TypeVar("T")

class BSTEntry(Generic[T]):
    def __init__(self, entry: T, key: int) -> None:
        self.entry = entry
        self.key = key

    def __repr__(self) -> str:
        return f"({self.entry}, {self.key})"