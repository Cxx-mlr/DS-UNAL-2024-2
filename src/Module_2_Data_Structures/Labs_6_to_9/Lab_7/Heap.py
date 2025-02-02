from __future__ import annotations

from typing_extensions import Optional, TypeVar, Iterable, Generic, overload
from abc import ABC, abstractmethod
import inspect

from pathlib import Path
import math

from List import List

T = TypeVar("T")
R = TypeVar("R")


class Heap(Generic[T], ABC):
    @staticmethod
    @abstractmethod
    def comparison(x: T, y: T) -> bool:
        pass

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, __iterable: Iterable[T]) -> None: ...

    def __init__(self, arg: Optional[Iterable[T]] = None) -> None:
        self.items = List[T](arg)

        for index in range(self.size() // 2)[::-1]:
            self._heapify(index=index, heap_size=self.size())

    def is_empty(self) -> bool:
        return self.items.is_empty()

    def push(self, value: T) -> None:
        self.items.push_back(value)
        current = len(self.items) - 1

        while current > 0 and self.__class__.comparison(
            self.items[current], self.items[self.parent(current)]
        ):
            parent_index = self.parent(current)
            self.items[current], self.items[parent_index] = (
                self.items[parent_index],
                self.items[current],
            )
            current = parent_index

    def pop(self) -> T:
        if len(self.items) == 0:
            raise IndexError("pop from an empty heap")

        max_value = self.items[0]
        self.items[0] = self.items[-1]
        self.items.pop_back()

        if len(self.items) > 0:
            self._heapify(index=0, heap_size=len(self.items))

        return max_value

    def size(self) -> int:
        return self.items.size()

    def __getitem__(self, index: int):
        return self.items[index]

    def __len__(self) -> int:
        return self.size()

    def __iter__(self):
        yield from self.items

    def parent(self, index: int) -> T:
        return math.ceil(index / 2) - 1

    def left(self, index: int) -> Optional[T]:
        return 2 * index + 1

    def right(self, index: int) -> Optional[T]:
        return 2 * index + 2

    def is_leaf(self, index: int):
        return self.left(index) >= self.size() or self.right() >= self.size()

    def _heapify(self, index: int, heap_size: int):
        largest = index
        left_index = self.left(index)
        right_index = self.right(index)

        if left_index < heap_size and self.__class__.comparison(
            self.items[left_index], self.items[largest]
        ):
            largest = left_index

        if right_index < heap_size and self.__class__.comparison(
            self.items[right_index], self.items[largest]
        ):
            largest = right_index

        if largest != index:
            self.items[index], self.items[largest] = (
                self.items[largest],
                self.items[index],
            )
            Heap._heapify(self, index=largest, heap_size=heap_size)

    def heap_sort(self):
        for i in range(len(self))[::-1]:
            self.items[0], self.items[i] = self.items[i], self.items[0]
            self._heapify(index=0, heap_size=i)

    def save_to_file(self, filename: Optional[str] = None):
        if filename is None:
            frame = inspect.currentframe().f_back
            try:
                reason = "Unable to determine a unique variable name for the heap instance. Please provide a filename explicitly."
                local_matches = [
                    name for name, value in frame.f_locals.items() if value is self
                ]
                if len(local_matches) == 1:
                    filename = f"{local_matches[0]}.d2"
                elif len(local_matches) > 1:
                    raise ValueError(reason)
                else:
                    global_matches = [
                        name for name, value in frame.f_globals.items() if value is self
                    ]
                    if len(global_matches) == 1:
                        filename = f"{global_matches[0]}.d2"
                    else:
                        raise ValueError(reason)
            finally:
                del frame

        declarations = []
        relationships = []

        if self.items.is_empty():
            declarations.append("\.:|md _|")

        for node_index in range(self.size()):
            declarations.append(
                f'{node_index}:"{self[node_index]}"' + " { shape: circle }"
            )

            if (left_child_index := self.left(node_index)) < self.size():
                relationships.append(f"{node_index} -> {left_child_index}")
            if (right_child_index := self.right(node_index)) < self.size():
                relationships.append(f"{node_index} -> {right_child_index}")

        output_path = Path(__file__).parent / filename
        with open(output_path, "wt", encoding="utf-8") as file:
            file.write(
                "\n".join(declarations)
                + ("\n\n" if relationships and declarations else "")
                + "\n".join(relationships)
            )

    def __repr__(self) -> str:
        return f"Heap({[v for v in self.items]})"


class MaxHeap(Heap[T]):
    @staticmethod
    def comparison(x: T, y: T) -> bool:
        return x > y

    def max(self) -> T:
        return self.items[0]


class MinHeap(Heap[T]):
    @staticmethod
    def comparison(x: T, y: T) -> bool:
        return x < y

    def min(self) -> T:
        return self.items[0]
