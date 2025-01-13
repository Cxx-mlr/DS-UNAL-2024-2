from rich import print as print

from Date import Date
from Address import Address
from User import User

from Agenda import Agenda


def main():
    user_1 = User(
        name="Juan-Perez",
        id=24567898,
        birth_date=Date(day=12, month=10, year=1980),
        birth_city="Medellin",
        phone_number="3003233234",
        email="juanperez@edl.edu.co",
        address=Address(
            street="kr74",
            nomenclature="4T-35",
            neighborhood="Boston",
            city="Medellin",
            building=None,
            apartment=None,
        ),
    )

    user_2 = User(
        name="Diego-Palacio",
        id=34568910,
        birth_date=Date(day=20, month=12, year=1979),
        birth_city="Envigado",
        phone_number="3013234567",
        email="diegopalacio@edl.edu.co",
        address=Address(
            street="cll65",
            nomenclature="3-29",
            neighborhood="Robledo",
            city="Medellin",
            building="Balcones-de-la-Quinta",
            apartment="405",
        ),
    )

    user_3 = User(
        name="Camila-Jimenez",
        id=2345902,
        birth_date=Date(day=15, month=9, year=1985),
        birth_city="Cali",
        phone_number="3003234567",
        email="camilajimenez@edl.edu.co",
        address=Address(
            street="tr45",
            nomenclature="4S-73",
            neighborhood="Poblado",
            city="Medellin",
            building=None,
            apartment=None,
        ),
    )

    user_4 = User(
        name="Pedro-Gomez",
        id=1075689,
        birth_date=Date(day=20, month=2, year=1990),
        birth_city="Popayan",
        phone_number="3003012323",
        email="pedrogomez@edl.edu.co",
        address=Address(
            street="kr23",
            nomenclature="8-10",
            neighborhood="SanJuan",
            city="Envigado",
            building="Mirador",
            apartment="503",
        ),
    )

    user_5 = User(
        name="Tatiana-Ramirez",
        id=2345934,
        birth_date=Date(day=15, month=11, year=1982),
        birth_city="Medellin",
        phone_number="3004567890",
        email="tatianaramirez@edl.edu.co",
        address=Address(
            street="cll5",
            nomenclature="4S-69",
            neighborhood="Poblado",
            city="Medellin",
            building="UrbColina",
            apartment="1023",
        ),
    )

    agenda = Agenda(capacity=10)

    agenda.add_user(user_1)
    agenda.add_user(user_2)
    agenda.add_user(user_3)
    agenda.add_user(user_4)
    agenda.add_user(user_5)

    correct_user_id: int = 34568910
    # incorrect_user_id: int = 11111111

    index = agenda.find_user(user_id=correct_user_id)

    if index != -1:
        print(f"[green]User found at index: {index}[/]")
    else:
        print("[red]User not found[/]")

    agenda.save_to_file()


if __name__ == "__main__":
    main()
