from __future__ import annotations

import os
from auth import login


def main():
    session = login()
    while True:
        try:
            os.system("cls")
            session.display_menu()
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
