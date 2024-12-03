from __future__ import annotations

from typing_extensions import Optional

class Node:
    def __init__(self, data: object) -> Node:
        self.__next: Optional[Node] = None
        self.__data = data

    def set_data(self, new_data: object):
        self.__data == new_data

    def get_data(self) -> object:
        return self.__data
    
    def set_next(self, next: Node):
        self.__next = next

    def get_next(self) -> Node:
        return self.__next

    def __repr__(self) -> str:
        return (
            f"Node("
            f"data={self.__data!r}, "
            f"next={self.__next!r}"
            f")"
        )