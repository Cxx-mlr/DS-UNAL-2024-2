from enum import Enum, auto

from rich import print
from utils import console, ask_in_range

class Role:
    @staticmethod
    def ask() -> str:
        console.rule("Seleccione un Rol")
        print("1. Investigador")
        print("2. Administrador")
        print()
        return ("investigador", "administrador")[
            ask_in_range(
                range_=range(1, 3),
                variadic=False,
                msg="Por favor, ingrese 1 para 'Investigador' o 2 para 'Administrador': ",
                err_msg="Entrada no válida. Ingrese un número entre 1 y 2."
            ) - 1
        ]