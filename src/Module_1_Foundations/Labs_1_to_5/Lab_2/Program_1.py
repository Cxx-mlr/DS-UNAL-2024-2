from rich import print

from Date import Date
from Address import Address
from User import User

def main():
    birth_date = Date(day=1, month=8, year=2001)
    address = Address(
        street="Calle 54A",
        nomenclature="30-01",
        neighborhood="Boston",
        city="Medellín",
    )

    user = User(
        name="John Doe",
        id=1234567890,
        birth_date=birth_date,
        birth_city="Africa",
        phone_number=9876543210,
        email="user@example.com",
        address=address
    )

    print(f"[green]Fecha de nacimiento[/]\n{birth_date}\n")
    print(f"[green]Dirección de residencia[/]\n{address}\n")
    print(f"[green]Información personal y de contacto[/]\n{user}\n")

if __name__ == "__main__":
    main()