from rich import print
from utils import console, ask_in_range


class Role:
    @staticmethod
    def ask() -> str:
        console.print("[yellow]Seleccione un Rol[/]")
        print("1. Investigador")
        print("2. Administrador")
        print()
        return ("investigador", "administrador")[
            ask_in_range(
                range_=range(1, 3),
                variadic=False,
                prompt="Por favor, ingrese [cyan]1[/] para [yellow]'Investigador'[/] o [cyan]2[/] para [yellow]'Administrador'[/]: ",
                error_message="Entrada no válida. Ingrese un número entre 1 y 2.",
            )
            - 1
        ]
