from rich.console import Console
console = Console()

from rich import print

from typing_extensions import List, Union

from contextlib import suppress

def ask_integer(msg: str, err_msg: str):
    while True:
        value = None
        with suppress(Exception):
            print(f"[blue]{msg}[/]", end="", flush=True)
            value = int(input(""))

        if value is None:
            print()
            print(f"[yellow]{err_msg}[/]")
        else:
            break

    return value

def ask_in_range(range_: range, variadic: bool, msg: str, err_msg: str) -> Union[int, List[int]]:
    while variadic:
        values = None
        with suppress(Exception):
            print(f"[blue]{msg}[/]", end="", flush=True)
            values = list(map(int, input("").split(" ")))

        if values is None:
            print()
            print(f"[yellow]{err_msg}[/]")
        else:
            if all(value in range_ for value in values):
                return values
            else:
                print()
                print(f"[yellow]{err_msg}[/]")

    while not variadic:
        value = ask_integer(msg, err_msg)
        if value not in range_:
            print()
            print(f"[yellow]{err_msg}[/]")
        else:
            return value