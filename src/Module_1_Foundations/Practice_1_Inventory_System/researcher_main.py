from __future__ import annotations

import os
from auth import login


def main():
    # Investigador
    user_id = 45678923
    password = "lV1983Bogo$"

    # Administrador
    user_id = 78904561
    password = "aC1992#Buca"

    session = login(user_id=user_id, password=password)
    while True:
        try:
            os.system("cls")
            session.display_menu()
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
