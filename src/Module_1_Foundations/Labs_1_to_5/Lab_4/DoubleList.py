from __future__ import annotations

from typing_extensions import Optional
from DoubleNode import DoubleNode

class DoubleList:
    def __init__(self) -> DoubleList:
        self.__head: Optional[DoubleNode] = None
        self.__tail: Optional[DoubleNode] = None

        self.__size: int = 0

    def size(self) -> int:
        return self.__size
    
    def set_size(self, new_size: int):
        raise NotImplementedError()
    
    def is_empty(self) -> bool:
        return self.__head is None

    def first(self) -> Optional[DoubleNode]:
        return self.__head

    def last(self) -> Optional[DoubleNode]:
        return self.__tail

    def add_first(self, data: object) -> Optional[DoubleNode]:
        node = DoubleNode(data=data)

        if self.__head is None:
            self.__head = node
            self.__tail = node
        else:
            self.__head.set_prev(node)
            node.set_next(self.__head)
            self.__head = node

        self.__size += 1

    def add_last(self, data: object) -> Optional[DoubleNode]:
        node = DoubleNode(data=data)

        if self.__tail is None:
            self.__head = node
            self.__tail = node
        else:
            node.set_prev(self.__tail)
            self.__tail.set_next(node)
            self.__tail = node

        self.__size += 1

    def find(self, data: object) -> Optional[DoubleNode]:
        if self.is_empty():
            return None

        node = self.__head
        while node.get_data() is not data:
            node = node.get_next()

            if node is None:
                return None
            
        return node

    def add_after(self, node: DoubleNode, data: object):
        new_node = DoubleNode(data)

        if (next := node.get_next()) is None:
            node.set_next(new_node)
            new_node.set_prev(node)

        else:
            node.set_next(new_node)
            new_node.set_next(next)

            next.set_prev(new_node)
            new_node.set_prev(node)

    def add_before(self, node: DoubleNode, data: object):
        new_node = DoubleNode(data)

        if (prev := node.get_prev()) is None:
            node.set_prev(new_node)
            new_node.set_next(node)

        else:
            node.set_prev(new_node)
            new_node.set_prev(prev)

            prev.set_next(new_node)
            new_node.set_next(node)

    def remove_first(self) -> Optional[DoubleNode]:
        if self.__head is None:
            raise RuntimeError("Cannot remove from an empty list")
        
        if self.__head is self.__tail:
            removed_node = self.__head

            self.__head = None
            self.__tail = None

        else:
            removed_node = self.__head

            self.__head.set_next(self.__head.get_next())
            removed_node.__next = None

            removed_node.set_next(None)

        self.__size -= 1
        return removed_node.__data
    
    def remove_last(self) -> Optional[DoubleNode]:
        if self.__tail is None:
            raise RuntimeError("Cannot remove from an empty list")

        if self.__head is self.__tail:
            removed_node = self.__head

            self.__head = None
            self.__tail = None
        else:
            removed_node = self.__tail
            node = removed_node.get_prev()

            node.set_next(None)
            self.__tail = node

            removed_node.set_prev(None)

        self.__size -= 1
        return removed_node.get_data()
    
    def remove(self, data: object) -> Optional[DoubleNode]:
        if self.is_empty():
            raise RuntimeError("Cannot remove from an empty list")
        
        node = self.__head

        if node.get_data() == data:
            return self.remove_first()
        
        while (next := node.get_next()) is not None and next.get_data() != data:
            node = next

        if next is None: return None

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
            f"size={self.__size}"
            f")"
        )
    
    def __str__(self) -> str:
        if self.is_empty():
            return "Empty List"
        
        output = "None ← "

        node = self.__head
        while node != None:
            node_labels = tuple()

            if node is self.__head:
                node_labels += ("head",)

            if node is self.__tail:
                node_labels += ("tail",)

            output += f"[{node.get_data()!r}]{node_labels if node_labels else ''} {'⇄ ' if node.get_next() is not None else ''}"
            node = node.get_next()
            
        output += "→ None"
        return output