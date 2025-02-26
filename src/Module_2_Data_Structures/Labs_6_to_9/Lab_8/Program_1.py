from BinarySearchTree import BinarySearchTree
from dataclasses import dataclass

@dataclass
class User:
    name: str
    id: int

    @property
    def key(self) -> int:
        return sum(map(int, str(self.id)))
    
    def __repr__(self) -> str:
        return f"{self.name} {self.id}"
        

def main():
    bstree = BinarySearchTree[User]()
    users = (
        User(name="Juan", id=10101013),
        User(name="Juan", id=10101567),
        User(name="Pablo", id=10001011),
        User(name="Maria", id=10101015),
        User(name="Ana", id=1010000),
        User(name="Diana", id=10111105),
        User(name="Mateo", id=10110005)
    )

    for user in users:
        bstree.insert(entry=user, key=user.key)

    bstree.save_to_file("users.d2")
    print(f"min: {bstree.min()}")
    print(f"max: {bstree.max()}\n")

    for node in bstree.in_order_iter():
        print(node.data)

    input()
    removed_node = bstree.find(key=7)
    bstree.remove(key=removed_node.data.key)
    print(f"Se ha eliminado {removed_node}")
    bstree.save_to_file("users.d2")


if __name__ == "__main__":
    main()