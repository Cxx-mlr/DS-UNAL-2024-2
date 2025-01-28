from __future__ import annotations

from typing_extensions import (
    Optional,
    Generic,
    TypeVar,
    Callable,
    Iterable,
    Union,
    Self,
    Any,
    overload,
)

from Node import Node

T = TypeVar("T")
R = TypeVar("R")


class List(Generic[T]):
    T: T

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, __iterable: Iterable[T]) -> None: ...

    def __init__(self, arg: Optional[Iterable[T]] = None) -> None:
        self.__head: Optional[Node[T]] = None
        self.__tail: Optional[Node[T]] = None
        self.__size: int = 0

        if isinstance(arg, List):
            node = arg.__head
            while node is not None:
                self.push_back(node.get_data())
                node = node.get_next()

        elif isinstance(arg, Iterable):
            for value in arg:
                self.push_back(value)

    def clone(self) -> List[T]:
        return List[T](self)

    def loose_clone(self) -> List[T]:
        return List[T]()

    def __add__(self, iterable: Iterable[T]) -> Self[T]:
        result_list = self.clone()
        result_list.extend(iterable)

        return result_list

    def __sub__(self, iterable: Iterable[T]) -> Self[T]:
        values = tuple(iterable)

        return self.filter_if(lambda value: value in values)

    def extend(self, iterable: Iterable[T], /):
        for item in iterable:
            self.push_back(item)

    def nodes(self):
        node = self.begin()
        while node is not None:
            yield node
            node = node.get_next()

    def begin(self) -> Node[T]:
        return self.__head

    def end(self) -> Node[T]:
        return self.__tail

    def clear(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    def for_each(self, func: Callable[[T], None]):
        for value in self:
            func(value)

    @overload
    def apply(self, func: Callable[[T], R]) -> List[R]: ...

    @overload
    def apply(self, func: Callable[[T], T]) -> Self[T]: ...

    def apply(self, func) -> List[R]:
        if self.empty():
            return self.loose_clone()

        front_result = func(self.front())
        if isinstance(front_result, self.__class__.T):
            result_list = self.loose_clone()
        else:
            result_list = List[R]()

        result_list.push_back(front_result)

        for node in self.begin() + 1:
            result_list.push_back(func(node.get_data()))

        return result_list

    def __iter__(self):
        for node in self.nodes():
            yield node.get_data()

    def __getitem__(self, index: int) -> T:
        return self.node_at(index).get_data()

    def __setitem__(self, index: int, data: T):
        self.node_at(index).set_data(data)

    def node_at(self, index: int) -> Node[T]:
        if index < 0:
            index = self.__size - abs(index)

        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")

        node = self.__head
        for _ in range(index):
            node = node.get_next()

        return node

    def size(self) -> int:
        return self.__size

    def is_empty(self) -> bool:
        return self.size() == 0

    def empty(self) -> bool:
        return self.__head is None

    def front(self) -> T:
        if self.__head is None:
            raise IndexError("Cannot access the first element of an empty list.")
        return self.__head.get_data()

    def back(self) -> T:
        if self.__tail is None:
            raise IndexError("Cannot access the last element of an empty list.")
        return self.__tail.get_data()

    def push_front(self, data: T):
        new_node = Node[T](data=data)

        if self.__head is None:
            self.__head = new_node
            self.__tail = new_node
        else:
            new_node.set_next(self.__head)
            self.__head = new_node

        self.__size += 1

    def push_back(self, data: T):
        new_node = Node[T](data=data)

        if self.__tail is None:
            self.__head = new_node
            self.__tail = new_node
        else:
            self.__tail.set_next(new_node)
            self.__tail = new_node

        self.__size += 1

    def pop_front(self) -> T:
        if self.__head is None:
            raise RuntimeError("Cannot remove from an empty list")

        data = self.__head.get_data()
        self.__head = self.__head.get_next()
        if self.__head is None:
            self.__tail = None
        self.__size -= 1
        return data

    def pop_back(self) -> T:
        if self.__tail is None:
            raise RuntimeError("Cannot remove from an empty list")

        if self.__head is self.__tail:
            data = self.__tail.get_data()
            self.__head = None
            self.__tail = None
        else:
            current = self.__head
            while current.get_next() is not self.__tail:
                current = current.get_next()
            data = self.__tail.get_data()
            current.set_next(None)
            self.__tail = current

        self.__size -= 1
        return data

    def find(self, data: Optional[T]) -> Optional[Node[T]]:
        node: Optional[Node[T]] = self.__head
        while node is not None and node.get_data() != data:
            node = node.get_next()

        return node

    def find_if(self, pred: Callable[[T], bool]) -> Optional[Node[T]]:
        node: Optional[Node[T]] = self.__head
        while node is not None and not pred(node.get_data()):
            node = node.get_next()

        return node

    def filter(self, data: T) -> Self[T]:
        filtered_list = self.loose_clone()

        for value in self:
            if value == data:
                filtered_list.push_back(value)

        return filtered_list

    def filter_if(self, pred: Callable[[T], bool]) -> List[T]:
        filtered_list = self.loose_clone()

        for data in self:
            if pred(data):
                filtered_list.push_back(data)
        return filtered_list

    def index(self, data: Optional[T]) -> int:
        i = 0

        node: Optional[Node[T]] = self.__head
        while node is not None and node.get_data() is not data:
            node = node.get_next()
            i += 1

        if node is not None:
            return i
        return -1

    def index_if(self, pred: Callable[[T], bool]) -> int:
        i = 0

        node: Optional[Node[T]] = self.__head
        while node is not None and not pred(node.get_data()):
            node = node.get_next()
            i += 1

        if node is not None:
            return i
        return -1

    def remove(self, data: T, count: int = 1) -> None:
        self.__init__(self.filter_if(lambda l_data: l_data != data))

    def remove_if(self, pred: Callable[[T], bool], count: int = 1) -> None:
        self.__init__(self.filter_if(lambda l_data: not pred(l_data)))

    @overload
    def insert(self, index: int, data: T): ...

    @overload
    def insert(self, index: int, data: Iterable[T]): ...

    @overload
    def insert(self, index: int, data: List[T]): ...

    def insert(self, index: int, data: Union[T, Iterable[T], List[T]]):
        if index < 0:
            index = self.__size - abs(index)

        if index < 0 or index > self.__size:
            raise IndexError("Index out of range")

        if isinstance(data, List):
            for value in data:
                self.insert(index, value)
                index += 1
        elif isinstance(data, Iterable) and not isinstance(data, str):
            for value in data:
                self.insert(index, value)
                index += 1
        else:
            if index == 0:
                self.push_front(data)
            elif index == self.__size:
                self.push_back(data)
            else:
                node = self.__head
                for _ in range(index - 1):
                    node = node.get_next()
                self.add_after(node, data)
                self.__size += 1

    def has(self, node: Node[T]) -> bool:
        for selfnode in self.nodes():
            if selfnode is node:
                return True

        return False

    def add_after(self, node: Node[T], data: T):
        if not self.has(node):
            raise ValueError("The specified node is not in the list")
        
        if node is self.__tail:
            self.push_back(data)
        else:
            new_node = Node[T](data)
            new_node.set_next(node.get_next())

            node.set_next(new_node)
            self.__size += 1

    def add_before(self, node: Node[T], data: T):
        if node is self.__head:
            self.push_front(data)
        else:
            new_node = Node[T](data)
            prev_node = self.__head
            while prev_node.get_next() is not node:
                prev_node = prev_node.get_next()

                if prev_node is None:
                    raise ValueError("The specified node is not in the list")
            new_node.set_next(node)
            prev_node.set_next(new_node)
            self.__size += 1

    @overload
    def erase(self, __node: Optional[Node[T]]) -> None: ...

    @overload
    def erase(self, __first: Optional[Node[T]], __last: Optional[Node[T]]) -> None: ...

    def erase(self, *args: Optional[Node[T]]) -> None:
        """
        Erases nodes from the original list.
        This method can be called with one or two arguments:
        - If called with one argument, it erases the specified node from the list.
        - If called with two arguments, it erases all nodes from the first node up to and including the last node.
        Args:
            *args: Optional[Node[T]] - One or two nodes to be erased from the list.
        Note:
            - If the node to be erased is the head or tail of the list, the corresponding pop_front or pop_back method is called.
            - If the range of nodes to be erased is specified, all nodes within that range are removed.
        """

        if len(args) == 1:
            __node = args[0]
            print(f"__node: {__node}")
            
            if __node is None:
                return
            if not isinstance(__node, Node):
                raise ValueError("The specified argument is not an instance of Node")
            
            if __node is self.__head:
                self.pop_front()
            elif __node is self.__tail:
                self.pop_back()
            else:
                prev_node = self.__head
                while prev_node is not None and prev_node.get_next() is not __node:
                    prev_node = prev_node.get_next()
                if prev_node is not None:
                    prev_node.set_next(__node.get_next())
                self.__size -= 1
        elif len(args) == 2:
            __first, __last = args
            if __first is None and __last is None:
                return
            if __first is __last:
                self.erase(__first)
                return
            if __first is None:
                current = self.__head
                while current is not None and current is not __last:
                    next_node = current.get_next()
                    self.erase(current)
                    current = next_node
                if current is __last:
                    self.erase(current)
            elif __last is None:
                current = __first
                while current is not None:
                    next_node = current.get_next()
                    self.erase(current)
                    current = next_node
            else:
                current = __first
                while current is not None and current is not __last:
                    next_node = current.get_next()
                    self.erase(current)
                    current = next_node
                if current is __last:
                    self.erase(current)

    def erase_if(self, pred: Callable[[T], bool]) -> None:
        current = self.__head
        while current is not None:
            next_node = current.get_next()
            if pred(current.get_data()):
                self.erase(current)
            current = next_node

    def sort(self, key: Optional[Callable[[T], Any]] = None):
        if key is None:
            def key(arg):
                return arg

        if self.__size > 1:
            sorted_head = None
            current = self.__head

            while current is not None:
                next_node = current.get_next()

                if sorted_head is None or key(sorted_head.get_data()) >= key(current.get_data()):
                    current.set_next(sorted_head)
                    sorted_head = current
                else:
                    sorted_current = sorted_head
                    while sorted_current.get_next() is not None and key(sorted_current.get_next().get_data()) < key(current.get_data()):
                        sorted_current = sorted_current.get_next()

                    current.set_next(sorted_current.get_next())
                    sorted_current.set_next(current)

                current = next_node

            self.__head = sorted_head
            self.__tail = sorted_head
            while self.__tail.get_next() is not None:
                self.__tail = self.__tail.get_next()

    def sorted(self, key: Optional[Callable[[T], Any]] = None) -> Self[T]:
        new_list = self.clone()
        new_list.sort(key=key)
        return new_list

    def reverse(self):
        prev = None
        current = self.__head
        self.__tail = self.__head
        while current is not None:
            next_node = current.get_next()
            current.set_next(prev)
            prev = current
            current = next_node
        self.__head = prev

    def reversed(self) -> Self[T]:
        new_list = self.clone()
        new_list.reverse()
        return new_list

    def __repr__(self) -> str:
        return "List([" + ", ".join(map(str, [value for value in self])) + "])"
