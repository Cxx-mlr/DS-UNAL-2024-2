
from typing_extensions import Generic, TypeVar, Optional, Iterable, overload

from List import List

T = TypeVar("T")

class Queue(Generic[T]):
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, __iterable: Iterable[T]) -> None: ...

    def __init__(self, arg: Optional[Iterable[T]] = None) -> None:
        self.items = List[T](arg)

    def size(self) -> int:
        return self.items.size()
    
    def is_empty(self) -> bool:
        return self.items.is_empty()

    def enqueue(self, data: T):
        self.items.push_back(data)

    def dequeue(self) -> T:
        return self.items.pop_front()
    
    def first(self) -> T:
        return self.items.front()
    
    def __iter__(self):
        yield from self.items
