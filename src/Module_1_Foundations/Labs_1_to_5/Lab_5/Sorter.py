from __future__ import annotations

from typing_extensions import Self, List, Optional
import random

class Sorter:
    def __init__(self, capacity: int) -> Self:
        self.__capacity = capacity
        self.__data = [None for _ in range(self.__capacity)]

    def initialize(self, a: int = -100, b: int = 100, unique: bool = False):
        if unique and (b - a + 1) < self.__capacity:
            raise ValueError("Range [a, b] is too small to generate the required number of unique values.")

        if unique:
            random_data = random.sample(range(a, b + 1), k=self.__capacity)
        else:
            random_data = random.choices(range(a, b + 1), k=self.__capacity)

        for index in range(self.__capacity):
            self.__data[index] = random_data[index]

    def bubble_sort(self):
        for i in range(self.__capacity):
            swap_occurred = False
            for j in range(self.__capacity - i - 1):
                if self.__data[j] > self.__data[j + 1]:
                    self.__data[j], self.__data[j + 1] = self.__data[j + 1], self.__data[j]
                    swap_occurred = True
            if not swap_occurred:
                break

    def selection_sort(self) -> None:
        for i in range(self.__capacity - 1):
            min_index = i
            for j in range(i + 1, self.__capacity):
                if self.__data[j] < self.__data[min_index]:
                    min_index = j
            self.__data[i], self.__data[min_index] = self.__data[min_index], self.__data[i]
                
    def insertion_sort(self) -> None:
        for i in range(1, self.__capacity):
            j = i - 1
            current_value = self.__data[i]
            while j >= 0 and self.__data[j] > current_value:
                self.__data[j + 1] = self.__data[j]
                j -= 1
            self.__data[j + 1] = current_value

    def __merge(self, left: int, middle: int, right: int):
        n1 = middle - left + 1
        n2 = right - middle

        L = [0] * n1
        R = [0] * n2

        for i in range(n1):
            L[i] = self.__data[left + i]
        for j in range(n2):
            R[j] = self.__data[middle + 1 + j]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.__data[k] = L[i]
                i += 1
            else:
                self.__data[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            self.__data[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            self.__data[k] = R[j]
            j += 1
            k += 1

    def __merge_sort_impl(self, left: int, right: int):
        if left < right:
            middle = (left + right) // 2

            self.__merge_sort_impl(left, middle)
            self.__merge_sort_impl(middle + 1, right)

            self.__merge(left, middle, right)

    def merge_sort(self, left: int = None, right: int = None):
        left = left or 0
        right = right or self.__capacity - 1

        self.__merge_sort_impl(left=left, right=right)

    def __binary_search_impl(self, value, left: int, right: int):
        if left > right:
            return -1
            
        middle = (left + right) // 2
        
        if value < self.__data[middle]:
            return self.__binary_search_impl(value, left, middle - 1)
        elif value > self.__data[middle]:
            return self.__binary_search_impl(value, middle + 1, right)
        else:
            return middle
        
    def binary_search(self, value: object, left: Optional[int] = None, right: Optional[int] = None) -> int:
        left = left or 0
        right = right or self.__capacity - 1

        return self.__binary_search_impl(value=value, left=left, right=right)
    
    def get_data(self) -> List:
        return self.__data

    def __repr__(self) -> str:
        return (
            "Sorter("
            f"capacity={self.__capacity!r}",
            ")"
        )
    
    def __str__(self) -> str:
        return f"{self.__data}"