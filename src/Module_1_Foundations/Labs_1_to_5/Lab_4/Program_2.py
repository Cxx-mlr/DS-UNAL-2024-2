from rich import print
from rich.console import Console

console = Console()

from List import List
from DoubleList import DoubleList

from Address import Address
from Date import Date
from User import User

from DoubleNode import DoubleNode

def ask_user(msg: str = "Ingrese los datos del usuario") -> User:
    print()
    console.rule(msg)
    print()

    name: str = input("Nombre: ")
    id: int = int(input("ID: ") or 0)
    email: str = input("Email: ")

    birth_date = input("Fecha de nacimiento (dd-mm-aa): ").split("-")
    if len(birth_date) == "3":
        day, month, year = birth_date.split("-")
    else:
        day = 1
        month = 1
        year = 2000

    birth_date = Date(day=int(day), month=int(month), year=int(year))

    birth_city = input("Ciudad de nacimiento: ")
    phone_number = int(input("Número de teléfono: ") or 0)

    print("\n-- Dirección --")
    street = input("Calle: ")
    nomenclature = input("Nomenclatura: ")
    neighborhood = input("Barrio: ")
    city = input("Ciudad: ")
    building = input("Edificio: ")
    apartment = input("Apartamento: ")

    address = Address(
        street=street,
        nomenclature=nomenclature,
        neighborhood=neighborhood,
        city=city,
        building=building,
        apartment=apartment
    )

    user = User(
        name=name,
        id=id,
        birth_date=birth_date,
        birth_city=birth_city,
        phone_number=phone_number,
        email=email,
        address=address
    )

    return user

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
            apartment=None
        )
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
            apartment="405"
        )
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
            apartment=None
        )
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
            apartment="503"
        )
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
            apartment="1023"
        )
    )

    console.rule("List")
    print()

    users_l = List()
    users_l.add_last(user_1)
    users_l.add_last(user_2)
    users_l.add_last(user_3)
    users_l.add_last(user_4)
    users_l.add_last(user_5)

    print(f"{users_l!r}")

    print()
    console.rule("DoubleList")
    print()

    users_dl = DoubleList()
    users_dl.add_last(user_1)
    users_dl.add_last(user_2)
    users_dl.add_last(user_3)
    users_dl.add_last(user_4)
    users_dl.add_last(user_5)

    print(f"{users_dl}")

    user_6 = ask_user("Ingrese un usuario para inserta al principio de la lista")
    user_7 = ask_user("Ingrese un usuario para inserta al final de la lista")

    users_l.add_first(user_6)
    users_l.add_last(user_7)

    users_dl.add_first(user_6)
    users_dl.add_last(user_7)

    print()
    console.rule("List")
    print()

    print(users_l)

    print()
    console.rule("DoubleList")
    print()

    print(users_dl)

    user_8 = ask_user("Ingrese un usuario para insertar después del tercer nodo en la lista doble")

    third_node = users_dl._DoubleList__head.get_next().get_next()
    users_dl.add_after(third_node, user_8)

    print()
    console.rule("DoubleList")
    print()

    print(users_dl)

if __name__ == "__main__":
    main()