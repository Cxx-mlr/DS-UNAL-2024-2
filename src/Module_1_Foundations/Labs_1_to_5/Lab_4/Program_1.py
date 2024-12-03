from rich import print
from rich.console import Console

from List import List
from DoubleList import DoubleList

console = Console()

def main():
    console.rule("List")
    print()

    values_l = List()

    values_l.add_first(6)
    values_l.add_first(4)

    for even in range(8, 21, 2):
        values_l.add_last(even)

    values_l.add_first(2)

    print(values_l)

    values_l.remove(1)
    values_l.remove(10)
    values_l.remove(20)

    print(values_l)
    print()

    console.rule("DoubleList")
    print()

    values_dl = DoubleList()

    values_dl.add_first(6)
    values_dl.add_first(4)

    for even in range(8, 21, 2):
        values_dl.add_last(even)

    values_dl.add_first(2)

    print(values_dl)

    values_dl.remove(1)
    values_dl.remove(10)
    values_dl.remove(20)

    print(values_dl)

if __name__ == "__main__":
    main()