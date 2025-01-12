from rich.console import Console
from rich import print

from typing_extensions import List, Union
from contextlib import suppress

console = Console()


def ask_integer(prompt: str, error_message: str):
    while True:
        value = None
        with suppress(Exception):
            print(f"[blue]{prompt}[/]", end="", flush=True)
            value = int(input(""))

        if value is None:
            print()
            print(f"[yellow]{error_message}[/]")
        else:
            break

    return value


def ask_string(prompt: str, error_message: str = ""):
    while True:
        value = None
        with suppress(Exception):
            print(f"[blue]{prompt}[/]", end="", flush=True)
            value = input("")

        if value is None:
            print()
            print(f"[yellow]{error_message}[/]")
        else:
            break

    return value


def ask_in_range(
    range_: range, variadic: bool, prompt: str, error_message: str
) -> Union[int, List[int]]:
    while variadic:
        values = None
        with suppress(Exception):
            print(f"[blue]{prompt}[/]", end="", flush=True)
            values = list(map(int, input("").split(" ")))

        if values is None:
            print()
            print(f"[yellow]{error_message}[/]")
        else:
            if all(value in range_ for value in values):
                return values
            else:
                print()
                print(f"[yellow]{error_message}[/]")

    while not variadic:
        value = ask_integer(prompt, error_message)
        if value not in range_:
            print()
            print(f"[yellow]{error_message}[/]")
        else:
            return value


def format_for_csv(value: str) -> str:
    return "_".join(f"{value}".split(" ")) if value != "None" else None


def format_from_csv(value: str) -> str:
    return "".join(f"{value}".split("_")) if value != "None" else None
