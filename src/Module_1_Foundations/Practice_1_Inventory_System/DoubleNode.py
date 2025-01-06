from __future__ import annotations

from typing_extensions import Optional

class DoubleNode:
    def __init__(self, data: Optional[object] = None) -> DoubleNode:
        self.__prev: Optional[DoubleNode] = None
        self.__next: Optional[DoubleNode] = None
        self.__data = data

    def set_data(self, new_data: object):
        self.__data = new_data

    def get_data(self) -> object:
        return self.__data
    
    def set_prev(self, prev: DoubleNode):
        self.__prev = prev

    def get_prev(self) -> DoubleNode:
        return self.__prev
    
    def set_next(self, next: DoubleNode):
        self.__next = next

    def get_next(self) -> DoubleNode:
        return self.__next

    def __repr__(self) -> str:
        return (
            f"Node("
            f"data={self.__data!r}, "
            # f"prev={self.__prev}"
            f"next={self.__next}"
            f")"
        )