from Heap import MaxHeap
from random import randint

h = MaxHeap(randint(14, 134) for _ in range(20))

h.push(111)
h.push(222)
h.push(333)

h.save_to_file(filename="h.d2")
print(f"El elemento mayor es: {h.max()}")

sh = MaxHeap(h)
sh.heap_sort()

print(f"El heap ordenado es: {sh}")

while not h.is_empty():
    input()
    print(f"Se ha eliminado {h.pop()}", end="", flush=True)
    h.save_to_file(filename="h.d2")
