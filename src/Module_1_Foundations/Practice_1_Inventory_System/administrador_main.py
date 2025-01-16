from __future__ import annotations

import os
from auth import login
from Session import Session
from utils import console

def main():
    session = Session()

    credentials_list = session.shared.credentials_list

    administrator_node = credentials_list.find_if(
        lambda credentials: credentials.is_administrator()
    )

    if administrator_node is None:
        console.print("Error: No se encontró ningún administrador en la lista de credenciales.")
        return

    administrator = administrator_node.get_data()

    session = login(user_id=administrator.get_user_id(), password=administrator.get_password())
    while True:
        try:
            os.system("cls")
            session.display_menu()
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
