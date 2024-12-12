from rich import print
from SorterList import SorterList

def main():
    sorter_list = SorterList()

    sorter_list.initialize(k=12)
    print("[bold red]Lista antes de ordenar:[/bold red]")
    print(sorter_list)

    sorter_list.sort()
    print("\n[bold green]Lista después de ordenar:[/bold green]")
    print(sorter_list)

if __name__ == "__main__":
    main()