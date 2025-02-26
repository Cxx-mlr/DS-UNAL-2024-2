from typing import TypeVar, Optional, Tuple
from BinaryTree import BinaryTree
from BSTEntry import BSTEntry
from Node import Node

T = TypeVar("T")


class BinarySearchTree(BinaryTree[BSTEntry[T]]):
    def find(self, key: int) -> Optional[Node[BSTEntry[T]]]:
        current = self._root

        while current is not None:
            if key == current.data.key:
                return current
            elif key < current.data.key:
                current = current.left
            else:
                current = current.right

        return None

    def insert(self, entry: T, key: int):
        new_node = Node(BSTEntry(entry, key))

        if self._root is None:
            self._root = new_node
            return

        current = self._root
        parent = None

        while current is not None:
            parent = current
            if key < current.data.key:
                current = current.left
            elif key > current.data.key:
                current = current.right
            else:
                raise ValueError(f"Duplicate key: {key}")

        if key < parent.data.key:
            parent.left = new_node
        else:
            parent.right = new_node

    def remove(self, key: int) -> T:
        self._root, removed_entry = self._remove_recursively(self._root, key)
        if removed_entry is None:
            raise KeyError(f"Key {key} not found in the tree")
        return removed_entry

    def _remove_recursively(
        self, node: Optional[Node[BSTEntry[T]]], key: int
    ) -> Tuple[Optional[Node[BSTEntry[T]]], Optional[T]]:
        if node is None:
            return None, None

        if key < node.data.key:
            node.left, removed_entry = self._remove_recursively(node.left, key)
        elif key > node.data.key:
            node.right, removed_entry = self._remove_recursively(node.right, key)
        else:
            removed_entry = node.data.entry

            if node.left is None:
                return node.right, removed_entry
            elif node.right is None:
                return node.left, removed_entry

            min_larger_node = self._find_min(node.right)
            node.data = min_larger_node.data
            node.right, _ = self._remove_recursively(
                node.right, min_larger_node.data.key
            )

        return node, removed_entry

    def _find_min(self, node: Node[BSTEntry[T]]) -> Node[BSTEntry[T]]:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _find_max(self, node: Node[BSTEntry[T]]) -> Node[BSTEntry[T]]:
        current = node
        while current.right is not None:
            current = current.right
        return current

    def min(self) -> T:
        if self.is_empty():
            raise ValueError("The tree is empty")

        return self._find_min(self._root).data.entry

    def max(self) -> T:
        if self.is_empty():
            raise ValueError("The tree is empty")

        return self._find_max(self._root).data.entry
