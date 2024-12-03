from rich import print

from Date import Date
from Address import Address
from User import User

def main():
    name: str = input("Nombre: ")
    id_: int = int(input("ID: "))
    email: str = input("Email: ")

    birth_date = input("Fecha de nacimiento (dd-mm-aa): ")
    day, month, year = birth_date.split("-")
    birth_date = Date(day=int(day), month=int(month), year=int(year))

    birth_city = input("Ciudad de nacimiento: ")
    phone_number = int(input("Número de teléfono: "))

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
        id=id_,
        birth_date=birth_date,
        birth_city=birth_city,
        phone_number=phone_number,
        email=email,
        address=address
    )

    print(f"\n[green]Información personal y de contacto[/]\n{user}\n")

if __name__ == "__main__":
    main()