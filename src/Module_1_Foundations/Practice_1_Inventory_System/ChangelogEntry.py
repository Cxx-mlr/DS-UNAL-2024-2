from __future__ import annotations

from typing_extensions import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from Equipment import Equipment
    from Request import Request

from UserList import UserList
from Inventory import Inventory
from User import User
from RequestList import RequestList
from DateTime import DateTime

from config import (
    EMPLOYEES_PATH,
    SAVED_INVENTORY_PATH,
    DELETED_INVENTORY_PATH,
    ADD_REQUESTS_PATH,
    DELETE_REQUESTS_PATH,
)


class ChangelogEntry:
    def __init__(
        self,
        user_id: Optional[int] = None,
        serial_number: Optional[int] = None,
        action: Optional[Literal["agregar", "eliminar"]] = None,
        date_time: Optional[DateTime] = None,
        status: Optional[Literal["PENDING", "APPROVED", "REJECTED"]] = None,
    ) -> ChangelogEntry:
        self.__status = status
        self.__user_id = user_id
        self.__serial_number = serial_number
        self.__action = action
        self.__date_time = date_time
        self.__status = status

    def get_request(self) -> Request:
        from Request import Request

        user = self.get_user()
        equipment = self.get_equipment()

        request = Request(
            username=user.get_name(),
            user_id=self.get_user_id(),
            name=equipment.get_name(),
            serial_number=equipment.get_serial_number(),
            purchase_date=equipment.get_purchase_date(),
            price=equipment.get_price(),
        )
        request.set_action(self.get_action())
        return request

    def get_user(self) -> User:
        with UserList(filename=EMPLOYEES_PATH) as users:
            node = users.find_if(lambda user: user.get_id() == self.get_user_id())

            if node is None:
                return User(id=self.get_user_id())

            return node.get_data()

    def get_equipment(self) -> Equipment:
        from Equipment import Equipment

        with (
            Inventory(filename=SAVED_INVENTORY_PATH) as saved_inventory,
            Inventory(filename=DELETED_INVENTORY_PATH) as deleted_inventory,
            RequestList(filename=ADD_REQUESTS_PATH) as add_requests,
            RequestList(filename=DELETE_REQUESTS_PATH) as remove_requests,
        ):
            node = (
                saved_inventory.find_if(
                    lambda item: item.get_serial_number() == self.get_serial_number()
                )
                or deleted_inventory.find_if(
                    lambda item: item.get_serial_number() == self.get_serial_number()
                )
                or add_requests.find_if(
                    lambda request: (
                        request.get_serial_number() == self.get_serial_number()
                        and request.get_user_id() == self.get_user_id()
                    )
                )
                or remove_requests.find_if(
                    lambda request: (
                        request.get_serial_number() == self.get_serial_number()
                        and request.get_user_id() == self.get_user_id()
                    )
                )
            )

            if node is None:
                return Equipment(serial_number=self.get_serial_number())

            return node.get_data().get_equipment()

    def get_user_id(self) -> Optional[int]:
        return self.__user_id

    def get_serial_number(self) -> Optional[int]:
        return self.__serial_number

    def get_action(self) -> Optional[Literal["agregar", "eliminar"]]:
        return self.__action

    def set_action(self, action: Literal["agregar", "eliminar"]):
        self.__action = action

    def get_date_time(self) -> Optional[DateTime]:
        return self.__date_time

    def set_date_time(self, date_time: DateTime):
        self.__date_time = date_time

    def get_status(self) -> Optional[Literal["PENDING", "APPROVED", "REJECTED"]]:
        return self.__status

    def set_status(self, status: Literal["PENDING", "APPROVED", "REJECTED"]):
        self.__status = status

    def to_csv(self) -> str:
        return f"{self.__user_id} {self.__serial_number} {self.__action.capitalize()} {self.__date_time.to_csv()}"

    @staticmethod
    def from_csv(csv_string: str) -> ChangelogEntry:
        parts = csv_string.strip().split()
        if len(parts) != 9:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 9 partes separadas por espacios, pero se obtuvieron {len(parts)} partes: {parts}"
            )

        try:
            user_id = int(parts[0]) if parts[0] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'user_id' a un entero. Valor proporcionado: {parts[0]}"
            )

        try:
            serial_number = int(parts[1]) if parts[1] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'serial_number' a un entero. Valor proporcionado: {parts[1]}"
            )

        action = parts[2].lower() if parts[2] != "None" else None
        if action is not None and action not in ("agregar", "eliminar"):
            raise ValueError(
                f"El valor de 'action' debe ser 'agregar' o 'eliminar'. Valor proporcionado: {action}"
            )

        try:
            date_time = DateTime.from_csv(" ".join(parts[3:9]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'DateTime' de las partes {parts[3:9]}. Error: {e}"
            )

        return ChangelogEntry(
            user_id=user_id,
            serial_number=serial_number,
            action=action,
            date_time=date_time,
        )

    def __str__(self) -> str:
        return self.to_csv()
