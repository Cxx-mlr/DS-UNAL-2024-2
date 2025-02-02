from __future__ import annotations
from typing import Generic, Tuple, Optional, Iterable, TypeVar, Union, overload
from dataclasses import dataclass

from Heap import MaxHeap


T = TypeVar("T")


@dataclass
class PriorityItem(Generic[T]):
    priority: int
    value: T

    def __gt__(self, other: PriorityItem[T]) -> bool:
        return self.priority > other.priority

    def __lt__(self, other: PriorityItem[T]) -> bool:
        return self.priority < other.priority

    def __eq__(self, other: PriorityItem[T]) -> bool:
        return self.priority == other.priority

    def __getitem__(self, index: int) -> Union[int, T]:
        if index == 0:
            return self.priority
        elif index == 1:
            return self.value
        else:
            raise IndexError("Index out of range")

    def __iter__(self):
        yield self.priority
        yield self.value

    def __str__(self) -> str:
        return f"({self.priority}, {self.value!r})"


class PriorityQueue(Generic[T]):
    @overload
    def __init__(self): ...

    def __init__(self, items: Optional[Iterable[Tuple[int, T]]] = None):
        self.heap = MaxHeap(
            [PriorityItem(priority=p, value=v) for p, v in items] if items else []
        )

    def enqueue(self, priority: int, value: T) -> None:
        self.heap.push(PriorityItem(priority, value))

    def dequeue(self) -> T:
        if len(self.heap) == 0:
            raise IndexError("dequeue from an empty priority queue")

        return self.heap.pop()[1]

    def peek(self) -> T:
        if len(self.heap) == 0:
            raise IndexError("peek from an empty priority queue")
        return self.heap.items[0][1]

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)

    def save_to_file(self, filename: Optional[str] = None):
        self.heap.save_to_file(filename=filename)

    def __repr__(self) -> str:
        return f"PriorityQueue({[(priority, value) for priority, value in self.heap.items]})"
