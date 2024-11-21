from rich import print
from pathlib import Path
import re

def main():
    print(f"[green]Programa 2[/]\n")

    with open(Path(__file__).parent / "test_pr2.txt", "rt", encoding="utf-8") as fp:
        paragraphs = fp.read().split("\n\n")

        total = 0

        for paragraph_index, paragraph in enumerate(paragraphs, start=1):
            count = len(re.findall(r"\ben\b", paragraph, re.IGNORECASE))
            print(f"[bold cyan]Párrafo #{paragraph_index}[/]")
            print(f"La palabra [bold green]\"en\"[/] se repite [bold green]{count}[/] veces\n")

            total += count

        print(f"En total, la palabra [bold green]\"en\"[/] se repite [bold green]{total}[/] veces")

if __name__ == "__main__":
    main()