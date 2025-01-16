from __future__ import annotations

import os
from auth import login


def main():
    # Investigador
    user_id = 24567898
    password = "j4an1980$"

    # Administrador
    user_id = 2345902
    password = "c4100l485Cal$"

    session = login(user_id=user_id, password=password)
    while True:
        try:
            os.system("cls")
            session.display_menu()
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
