from __future__ import annotations
from typing_extensions import Self
from List import List
import random


class SorterList:
    def __init__(self) -> Self:
        self.__list: List = List()

    def initialize(
        self, k: int, *, a: int = -100, b: int = 100, unique: bool = False
    ) -> None:
        if unique and (b - a + 1) < k:
            raise ValueError(
                "Range [a, b] is too small to generate the required number of unique values."
            )

        if unique:
            random_data = random.sample(range(a, b + 1), k=k)
        else:
            random_data = random.choices(range(a, b + 1), k=k)

        for value in random_data:
            self.__list.add_last(value)

    def sort(self) -> None:
        if self.__list.is_empty():
            return

        current = self.__list.first()
        while current is not None:
            smallest = current
            next_node = current.get_next()

            while next_node is not None:
                if next_node.get_data() < smallest.get_data():
                    smallest = next_node
                next_node = next_node.get_next()

            current_data = current.get_data()
            smallest_data = smallest.get_data()

            current.set_data(smallest_data)
            smallest.set_data(current_data)

            current = current.get_next()

    def __str__(self) -> str:
        return f"{self.__list}"
