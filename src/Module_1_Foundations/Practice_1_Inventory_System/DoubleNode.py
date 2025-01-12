from __future__ import annotations

from typing_extensions import Optional, Generic, TypeVar

T = TypeVar("T")


class DoubleNode(Generic[T]):
    def __init__(self, data: T) -> None:
        self.__prev: Optional[DoubleNode[T]] = None
        self.__next: Optional[DoubleNode[T]] = None
        self.__data = data

    def set_data(self, data: T):
        self.__data = data

    def get_data(self) -> T:
        return self.__data

    def set_prev(self, prev: Optional[DoubleNode[T]]):
        self.__prev = prev

    def get_prev(self) -> Optional[DoubleNode[T]]:
        return self.__prev

    def set_next(self, next: Optional[DoubleNode[T]]):
        self.__next = next

    def get_next(self) -> Optional[DoubleNode[T]]:
        return self.__next

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DoubleNode):
            return self.__data == other.get_data()
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, index: int) -> DoubleNode[T]:
        node = self
        while index > 0:
            index -= 1
            node = node.get_next()

        return node

    def __sub__(self, index: int) -> DoubleNode[T]:
        node = self
        while index > 0:
            index -= 1
            node = node.get_prev()

        return node

    def __iter__(self):
        node = self
        while node is not None:
            yield node
            node = node.get_next()

    def __repr__(self) -> str:
        return f"DoubleNode({self.get_data()})"
