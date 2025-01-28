from PriorityQueue import PriorityQueue
import random

p = PriorityQueue()
items = [
    (9, "A"),
    (8, "B"),
    (7, "C"),
    (6, "D"),
    (5, "E"),
    (4, "F"),
    (3, "G"),
    (2, "H"),
    (1, "I"),
    (0, "J"),
]

random.shuffle(items)

for priority, item in items:
    p.enqueue(priority, item)

p.save_to_file(filename="p.d2")
print(f"El elemento con mayor prioridad es: {p.peek()}")

while not p.is_empty():
    input()
    print(f"Se ha eliminado: {p.dequeue()}", end="", flush=True)
    p.save_to_file(filename="p.d2")
