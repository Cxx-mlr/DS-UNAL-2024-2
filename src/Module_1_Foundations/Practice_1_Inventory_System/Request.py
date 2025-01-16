from __future__ import annotations

from typing_extensions import Literal, Optional, TYPE_CHECKING

from Date import Date
from Equipment import Equipment
from DateTime import DateTime

from config import (
    EMPLOYEES_PATH,
    ADD_REQUESTS_PATH,
    DELETE_REQUESTS_PATH,
)

from User import User

if TYPE_CHECKING:
    from InventoryItem import InventoryItem
    from ChangelogEntry import ChangelogEntry
    from Session import Session
    from RequestList import RequestList


class Request(Equipment):
    def __init__(
        self,
        username: Optional[str] = None,
        user_id: Optional[int] = None,
        name: Optional[str] = None,
        serial_number: Optional[int] = None,
        purchase_date: Optional[Date] = None,
        price: Optional[int] = None,
    ) -> Request:
        self.__action: Optional[Literal["agregar", "eliminar"]] = None
        self.__status: Optional[Literal["PENDING", "APPROVED", "REJECTED"]] = None
        self.__username = username
        self.__user_id = user_id
        super().__init__(
            name=name,
            serial_number=serial_number,
            purchase_date=purchase_date,
            price=price,
        )

    def purge(self, session: Session):
        requests: Optional[RequestList] = None

        if self.get_action() == "agregar":
            requests = session.shared.add_requests
        elif self.get_action() == "eliminar":
            requests = session.shared.delete_requests
        else:
            return

        requests.erase(requests.find(self))
        requests.save_to_file()

    def approve(self, session: Session):
        if self.get_action() is None:
            raise RuntimeError("Action must be set before approving the request.")

        saved_inventory = session.shared.saved_inventory
        deleted_inventory = session.shared.deleted_inventory
        approved_changelog = session.shared.approved_changelog

        if self.get_action() == "agregar":
            node = saved_inventory.find(item := self.get_item())
            if node is not None:
                print(
                    "No se ha agregado el equipo, dado que el equipo ya existe en el inventario."
                )
                return
            saved_inventory.push_back(item)
            deleted_inventory.erase_if(
                lambda deleted_item: deleted_item.get_user_id() == item.get_user_id()
                and deleted_item.get_serial_number() == item.get_serial_number()
            )

            self.purge(session=session)

        elif self.get_action() == "eliminar":
            node = saved_inventory.find(self.get_item())

            if node is None:
                print(
                    "No se ha eliminado el equipo, dado que el equipo no existe en el inventario."
                )
                return

            item = node.get_data()
            deleted_inventory.push_back(item)
            saved_inventory.erase(node)

            self.purge(session=session)

        approved_changelog.push_back(self.get_changelog_entry(status="APPROVED"))
        approved_changelog.save_to_file()

        saved_inventory.save_to_file()
        deleted_inventory.save_to_file()

    def reject(self, session: Session):
        if self.get_action() is None:
            raise RuntimeError("Action must be set before rejecting the request.")

        rejected_changelog = session.shared.rejected_changelog

        self.purge(session=session)

        rejected_changelog.push_back(self.get_changelog_entry(status="REJECTED"))
        rejected_changelog.save_to_file()

    def submit(self):
        from RequestList import RequestList

        if self.get_action() == "agregar":
            filename = ADD_REQUESTS_PATH
        elif self.get_action() == "eliminar":
            filename = DELETE_REQUESTS_PATH

        with RequestList(filename=filename) as requests:
            requests.push_back(self)
            requests.sorted(
                key=lambda request: request.get_serial_number()
            ).save_to_file()

    def get_item(self) -> InventoryItem:
        from InventoryItem import InventoryItem

        equipment = self.get_equipment()
        return InventoryItem(
            username=self.get_username(),
            user_id=self.get_user_id(),
            name=equipment.get_name(),
            serial_number=equipment.get_serial_number(),
            purchase_date=equipment.get_purchase_date(),
            price=equipment.get_price(),
        )

    def get_changelog_entry(
        self, status: Literal["PENDING", "APPROVED", "REJECTED"] = "PENDING"
    ) -> ChangelogEntry:
        from ChangelogEntry import ChangelogEntry

        equipment = self.get_equipment()
        return ChangelogEntry(
            user_id=self.get_user_id(),
            serial_number=equipment.get_serial_number(),
            action=self.get_action(),
            date_time=DateTime.now(),
            status=status,
        )

    def get_action(self) -> Optional[Literal["agregar", "eliminar"]]:
        return self.__action

    def set_action(self, action: Literal["agregar", "eliminar"]):
        self.__action = action

    def get_status(self) -> Optional[Literal["PENDING", "APPROVED", "REJECTED"]]:
        return self.__status

    def set_status(self, status: Optional[Literal["PENDING", "APPROVED", "REJECTED"]]):
        self.__status = status

    def get_user(self) -> User:
        from UserList import UserList

        with UserList(filename=EMPLOYEES_PATH) as users:
            node = users.find_if(lambda user: user.get_id() == self.get_user_id())

            if node is None:
                return User()

            return node.get_data()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Request):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other: object):
        return not self.__eq__(other)

    def get_equipment(self) -> Equipment:
        return Equipment(
            name=self.get_name(),
            serial_number=self.get_serial_number(),
            purchase_date=self.get_purchase_date(),
            price=self.get_price(),
        )

    def get_username(self) -> Optional[str]:
        return self.__username

    def get_user_id(self) -> Optional[str]:
        return self.__user_id

    def to_csv(self) -> str:
        return f"{self.__username} {self.__user_id} {super().to_csv()}"

    @staticmethod
    def from_csv(csv_string: str) -> Request:
        parts = csv_string.strip().split()

        if len(parts) < 8:
            raise ValueError(
                f"La cadena CSV debe contener exactamente 8 partes separadas por espacios, pero tiene {len(parts)} partes: {parts}"
            )

        try:
            username = parts[0]
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'username' de la cadena CSV. Partes: {parts}"
            )

        try:
            user_id = int(parts[1]) if parts[1] != "None" else None
        except ValueError:
            raise ValueError(
                f"No se pudo convertir 'user_id' a un entero. Valor proporcionado: {parts[1]}"
            )
        except IndexError:
            raise ValueError(
                f"No se pudo extraer 'user_id' de la cadena CSV. Partes: {parts}"
            )

        try:
            equipment = Equipment.from_csv(" ".join(parts[2:10]))
        except Exception as e:
            raise ValueError(
                f"No se pudo instanciar 'Equipment' de las partes {parts[2:10]}. Error: {e}"
            )

        return Request(
            username=username,
            user_id=user_id,
            name=equipment.get_name(),
            price=equipment.get_price(),
            purchase_date=equipment.get_purchase_date(),
            serial_number=equipment.get_serial_number(),
        )

    def __str__(self):
        user = self.get_user()
        equipment = self.get_equipment()

        request_repr = f"[yellow]{user.get_name()} ({user.get_id()})[/] solicita"

        if self.get_action() == "agregar":
            request_repr += " [green]agregar[/]"
        elif self.get_action() == "eliminar":
            request_repr += " [red]eliminar[/]"

        request_repr += f" {equipment.get_name()} ({equipment.get_serial_number()}) [green]$[{equipment.get_price()}][/]"
        return request_repr
