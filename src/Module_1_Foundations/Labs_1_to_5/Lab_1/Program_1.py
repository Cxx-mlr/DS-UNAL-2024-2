from rich import print

def main():
    print(f"[green]Programa 1[/]\n")

    n = int(input("n: "))

    values: list[int] = []

    for _ in range(n):
        values.append(
            int(input("Ingrese un número entero: "))
        )

    print(f"\nmínimo: {min(values)}")
    print(f"máximo: {max(values)}")
    print(f"suma: {sum(values)}")
    print(f"promedio: {round(sum(values) / len(values), 4)}")

if __name__ == "__main__":
    main()