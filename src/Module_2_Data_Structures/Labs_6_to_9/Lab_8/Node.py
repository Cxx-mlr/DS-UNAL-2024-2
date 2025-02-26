from __future__ import annotations

from typing_extensions import Optional, Generic, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.left: Optional[Node[T]] = None
        self.right: Optional[Node[T]] = None
        self.data = data

    def __repr__(self) -> str:
        return f"Node(data={self.data!r})"
