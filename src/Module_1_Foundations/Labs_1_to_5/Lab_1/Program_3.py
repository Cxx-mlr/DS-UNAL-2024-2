from rich import print

MAX_ATTEMPS = 3

ACCESS_GRANTED_MESSAGE = "[green]Acceso permitido.[/]"
ACCESS_DENIED_MESSAGE = "[yellow]Datos incorrectos.[/]"
ACCESS_BLOCKED_MESSAGE = "[red]Lo siento, su acceso no es permitido.[/]"

fake_db = {
    "Juan1223": "J12an*.",
    "Maria2345": "M23a*.",
    "Pablo1459": "P14o*.",
    "Ana3456": "A34a*"
}

def main():
    print("[green]Programa 3[/]\n")

    attempts_left = MAX_ATTEMPS

    while attempts_left > 0:
        attempts_left -= 1

        username = input("username: ")
        password = input("password: ")

        if username not in fake_db or fake_db[username] != password:
            print(ACCESS_DENIED_MESSAGE, end="\n\n")
        else:
            print(ACCESS_GRANTED_MESSAGE)
            break
    else:
        print(ACCESS_BLOCKED_MESSAGE)

if __name__ == "__main__":
    main()