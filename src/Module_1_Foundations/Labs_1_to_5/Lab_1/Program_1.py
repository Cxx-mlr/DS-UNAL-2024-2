from rich import print
from typing_extensions import List

def min_(values: List[int]) -> int:
    assert values, "min_() arg is an empty sequence"

    minimum = values[0]

    for value in values:
        if value < minimum:
            minimum = value

    return minimum

def max_(values: List[int]) -> int:
    assert values, "max_() arg is an empty sequence"

    maximum = values[0]

    for value in values:
        if value > maximum:
            maximum = value

    return maximum

def sum_(values: List[int]) -> int:
    total = 0

    for value in values:
        total += value

    return total

def average_(values: List[int]) -> int:
    if not values:
        return None

    return sum_(values) / len(values)

def main():
    print(f"[green]Programa 1[/]\n")

    n = int(input("Por favor, ingrese el número de datos que desea ingresar\n\n: "))

    values: list[int] = []

    print("\nA continuación, ingrese los números enteros uno por uno:\n")
    for i, _ in enumerate(range(n), start=1):
        values.append(
            int(input(f"{i}. Ingrese un número entero\n\n: "))
        )

        print()

    minimum = min_(values)
    maximum = max_(values)
    total = sum_(values)
    average = average_(values)

    print(f"\nMínimo: {minimum}")
    print(f"Máximo: {maximum}")
    print(f"Suma: {total}")
    print(f"Promedio: {average}")

if __name__ == "__main__":
    main()