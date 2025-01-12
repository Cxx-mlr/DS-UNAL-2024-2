from rich import print

from Agenda import Agenda


def main():
    agenda = Agenda(capacity=10)
    agenda.load_from_file()

    print(f"{agenda!s}")

    agenda.delete_user(user_id=2345934)
    agenda.save_to_file(filename="agenda2.txt")


if __name__ == "__main__":
    main()
