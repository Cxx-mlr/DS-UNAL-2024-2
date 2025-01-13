from __future__ import annotations

from typing_extensions import Optional
from Node import Node


class List:
    def __init__(self) -> List:
        self.__head: Optional[Node] = None
        self.__tail: Optional[Node] = None

        self.__size: int = 0

    def size(self) -> int:
        return self.__size

    def set_size(self, new_size: int):
        raise NotImplementedError()

    def is_empty(self) -> bool:
        return self.__size == 0

    def first(self) -> Optional[Node]:
        return self.__head

    def last(self) -> Optional[Node]:
        return self.__tail

    def add_first(self, data: object) -> Optional[Node]:
        node = Node(data=data)

        if self.__head is None:
            self.__head = node
            self.__tail = node
        else:
            node.set_next(self.__head)
            self.__head = node

        self.__size += 1

    def add_last(self, data: object) -> Optional[Node]:
        node = Node(data=data)

        if self.__tail is None:
            self.__head = node
            self.__tail = node
        else:
            self.__tail.set_next(node)
            self.__tail = node

        self.__size += 1

    def remove_first(self) -> Optional[Node]:
        if self.is_empty():
            raise RuntimeError("Cannot remove from an empty list")

        if self.__head is self.__tail:
            removed_node = self.__head

            self.__head = None
            self.__tail = None

        else:
            removed_node = self.__head
            self.__head = self.__head.get_next()

            removed_node.set_next(None)

        self.__size -= 1
        return removed_node

    def remove_last(self) -> Optional[Node]:
        if self.is_empty():
            raise RuntimeError("Cannot remove from an empty list")

        if self.__head is self.__tail:
            removed_node = self.__head

            self.__head = None
            self.__tail = None
        else:
            node = self.__head
            removed_node = self.__tail

            while (next := node.get_next()) is not removed_node:
                node = next

            node.set_next(None)
            self.__tail = node

        self.__size -= 1
        return removed_node

    def remove(self, data: object) -> Optional[Node]:
        if self.is_empty():
            raise RuntimeError("Cannot remove from an empty list")

        node = self.__head

        if node.get_data() == data:
            return self.remove_first()

        while (next := node.get_next()) is not None and next.get_data() != data:
            node = next

        if next is None:
            return None

        if next is self.__tail:
            return self.remove_last()

        node.set_next(next.get_next())
        next.set_next(None)

        return next

    def __repr__(self) -> str:
        return (
            f"List("
            f"head={self.__head!r}, "
            f"tail={self.__tail!r}, "
            f"size={self.__size!r}"
            f")"
        )

    def __str__(self) -> str:
        output = ""

        node = self.__head
        while node is not None:
            node_labels = tuple()

            if node is self.__head:
                node_labels += ("head",)

            if node is self.__tail:
                node_labels += ("tail",)

            output += f"[{node.get_data()!r}]{node_labels if node_labels else ''} → "
            node = node.get_next()

        output += "None"
        return output
