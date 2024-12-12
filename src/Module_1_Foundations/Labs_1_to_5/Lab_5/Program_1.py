from rich import print
from rich.console import Console

import operator
import random

from Sorter import Sorter

console = Console()

def main():
    sorter = Sorter(capacity=10)

    for sorting_method in (
        "bubble_sort",
        "selection_sort",
        "insertion_sort",
        "merge_sort"
    ):
        console.rule(" ".join(sorting_method.split("_")).title())
        sorter.initialize(10)

        print(sorter)
        operator.methodcaller(sorting_method)(sorter)
        print(sorter, end="\n\n")

    console.rule("Binary Search")

    sorter.initialize()
    sorter.merge_sort()
    value = random.choice(sorter.get_data())
    
    print(sorter, end="\n\n")
    print(f"[cyan]Iniciando búsqueda binaria del valor: {value}[/cyan]")
    index = sorter.binary_search(value)

    if index != -1:
        print(f"[bold green]Valor encontrado en el índice: {index}[/bold green]")
    else:
        print("[bold red]Valor no encontrado en la lista.[/bold red]")

if __name__ == "__main__":
    main()