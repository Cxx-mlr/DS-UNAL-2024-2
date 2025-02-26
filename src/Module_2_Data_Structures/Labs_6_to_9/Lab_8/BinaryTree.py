from typing_extensions import Generic, TypeVar, Optional, Iterator
from Node import Node
from collections import deque
from pathlib import Path
from uuid import uuid4

T = TypeVar("T")


class BinaryTree(Generic[T]):
    def __init__(self) -> None:
        self._root: Optional[Node[T]] = None
        self._size = 0

    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._root is None

    def is_root(self, node: Node[T]) -> bool:
        return node is self._root

    def is_leaf(self, node: Node[T]) -> bool:
        return node.left is None and node.right is None

    def is_internal(self, node: Node[T]) -> bool:
        if self.is_root(node) or self.is_leaf(node):
            return False
        return True

    def has_left(self, node: Node[T]) -> bool:
        return node.left is not None

    def has_right(self, node: Node[T]) -> bool:
        return node.right is not None

    def root(self) -> Optional[Node[T]]:
        return self._root

    def left(self, node: Node[T]) -> Optional[Node[T]]:
        return node.left

    def right(self, node: Node[T]) -> Optional[Node[T]]:
        return node.right

    def parent(self, node: Node[T]) -> Optional[Node[T]]:
        if node is self._root or self._root is None:
            return None

        queue = deque([self._root])

        while queue:
            current = queue.popleft()

            if current.left is node or current.right is node:
                return current

            if current.left is not None:
                queue.append(current.left)

            if current.right is not None:
                queue.append(current.right)

        return None

    def depth(self, node: Node[T]) -> int:
        if node is self._root:
            return 0
        return 1 + self.depth(self.parent(node))

    def height(self, node: Node[T]) -> int:
        if node is None:
            return -1
        left_height = self.height(node.left)
        right_height = self.height(node.right)
        return 1 + max(left_height, right_height)

    def add_root(self, data: T):
        new_root = Node[T](data)
        new_root.left = self._root
        self._root = new_root

        self._size += 1

    def insert_left(self, node: Node[T], data: T):
        new_node = Node[T](data)

        if node.left is None:
            node.left = new_node
        else:
            left_node = node.left
            node.left = new_node
            new_node.left = left_node
            
        self._size += 1

    def insert_right(self, node: Node[T], data: T):
        new_node = Node[T](data)

        if node.right is None:
            node.right = new_node
        else:
            right_node = node.right
            node.right = new_node
            new_node.right = right_node

        self._size += 1

    def insert(self, data: T):
        if self._root is None:
            self._root = Node[T](data)
            return

        queue = deque([self._root])

        while queue:
            temp = queue.popleft()

            if temp.left is None:
                temp.left = Node[T](data)
                break
            else:
                queue.append(temp.left)

            if temp.right is None:
                temp.right = Node[T](data)
                break
            else:
                queue.append(temp.right)

        self._size += 1

    def remove(self, node: Node[T]):
        parent_node = self.parent(node)
        new_child = node.left or node.right

        if node.left is not None and node.right is not None:
            new_child = None

        if parent_node.left is node:
            parent_node.left = new_child
            
        elif parent_node.right is node:
            parent_node.right = new_child

        self._size -= 1

    def pre_order_iter(self) -> Iterator[Node[T]]:
        if self._root is None:
            return iter([])

        stack = [self._root]

        while stack:
            current = stack.pop()
            yield current

            if current.right:
                stack.append(current.right)

            if current.left:
                stack.append(current.left)

    def in_order_iter(self) -> Iterator[Node[T]]:
        stack = []
        current: Optional[Node[T]] = self._root

        while stack or current is not None:
            while current is not None:
                stack.append(current)
                current = current.left

            current = stack.pop()
            yield current
            current = current.right

    def post_order_iter(self) -> Iterator[Node[T]]:
        if self._root is None:
            return iter([])
        
        stack1 = [self._root]
        stack2 = []

        while stack1:
            node = stack1.pop()
            stack2.append(node)

            if node.left:
                stack1.append(node.left)
                
            if node.right:
                stack1.append(node.right)

        while stack2:
            yield stack2.pop()

    def save_to_file(self, filename: str):
        output_path = Path(__file__).parent / filename

        declarations = []
        relationships = []

        if self._root is None:
            declarations.append("\.:|md _|")

        uuid_nodes = dict(zip(self.pre_order_iter(), iter(uuid4, None)))

        for node, uuid in uuid_nodes.items():
            left_node_uuid = uuid_nodes.get(node.left)
            right_node_uuid = uuid_nodes.get(node.right)
            
            declarations.append(
                f'{uuid}:"{node.data}"' + " { shape: circle }"
            )

            if node.left is not None:
                relationships.append(f"{uuid} -> {left_node_uuid}")
            if node.right is not None:
                relationships.append(f"{uuid} -> {right_node_uuid}")

            if sum((node.left is None, node.right is None)) == 1:
                if node.left is not None:
                    relationships[-1] += ": left"
                else:
                    relationships[-1] += ": right"

        with open(output_path, "wt", encoding="utf-8") as file:
            file.write(
                "\n".join(declarations)
                + ("\n\n" if relationships and declarations else "")
                + "\n".join(relationships)
            )

def parent(btree: BinaryTree[T], node: Node[T]) -> Optional[Node[T]]:
    if node is btree.root() or btree.root() is None:
        return None
    
    queue = deque([btree.root()])

    while queue:
        current = queue.popleft()

        if current.left is node or current.right is node:
            return current
        
        if current.left is not None:
            queue.append(current.left)

        if current.right is not None:
            queue.append(current.right)
