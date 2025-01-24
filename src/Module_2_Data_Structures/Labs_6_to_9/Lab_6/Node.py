from __future__ import annotations

from typing_extensions import Optional, Generic, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T) -> Node:
        self.__next: Optional[Node[T]] = None
        self.__data = data

    def set_data(self, data: T):
        self.__data = data

    def get_data(self) -> T:
        return self.__data

    def set_next(self, next: Optional[Node[T]]):
        self.__next = next

    def get_next(self) -> Optional[Node[T]]:
        return self.__next

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.__data == other.get_data()
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, index: int) -> Node[T]:
        node = self
        while index > 0:
            index -= 1
            node = node.get_next()

        return node

    def __iter__(self):
        node = self
        while node is not None:
            yield node
            node = node.get_next()

    def __repr__(self) -> str:
        return f"Node(" f"data={self.__data!r}, " f"next={self.__next!r}" f")"
