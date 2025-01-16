from __future__ import annotations

from typing_extensions import Literal, Optional
from pathlib import Path

from User import User
from Credentials import Credentials
from CredentialsList import CredentialsList
from RequestList import RequestList
from Inventory import Inventory
from Changelog import Changelog
from Equipment import Equipment
from UserList import UserList
from EquipmentList import EquipmentList

from config import (
    ADD_REQUESTS_PATH,
    DELETE_REQUESTS_PATH,
    PASSWORDS_PATH,
    SAVED_INVENTORY_PATH,
    DELETED_INVENTORY_PATH,
    APPROVED_CHANGE_CONTROL_PATH,
    REJECTED_CHANGE_CONTROL_PATH,
    EMPLOYEES_PATH,
)


class Session:
    def __init__(self, user: Optional[User] = None):
        self.__user = user
        self.shared = self.Shared(self)
        self.current = (
            self.Current(session=self, shared=self.shared) if user is not None else None
        )

    class Shared:
        def __init__(self, session: Session):
            self.__session = session

        @property
        def users(self) -> UserList:
            with UserList(filename=EMPLOYEES_PATH, session=self.__session) as users:
                return users

        @property
        def credentials_list(self) -> CredentialsList:
            with CredentialsList(filename=PASSWORDS_PATH) as credentials_list:
                return credentials_list

        @property
        def add_requests(self) -> RequestList:
            return self.__session._get_requests(
                ADD_REQUESTS_PATH, "PENDING", "agregar", filter_by_user=False
            )

        @property
        def delete_requests(self) -> RequestList:
            return self.__session._get_requests(
                DELETE_REQUESTS_PATH, "PENDING", "eliminar", filter_by_user=False
            )

        @property
        def pending_requests(self) -> RequestList:
            return self.add_requests + self.delete_requests

        @property
        def approved_requests(self) -> RequestList:
            return self.approved_changelog.apply(lambda entry: entry.get_request())

        @property
        def rejected_requests(self) -> RequestList:
            return self.rejected_changelog.apply(lambda entry: entry.get_request())

        @property
        def non_pending_requests(self) -> RequestList:
            return self.approved_requests + self.rejected_requests

        @property
        def requests(self) -> RequestList:
            return self.pending_requests + self.non_pending_requests

        @property
        def saved_inventory(self) -> Inventory:
            return self.__session._get_inventory(
                SAVED_INVENTORY_PATH, filter_by_user=False
            )

        @property
        def deleted_inventory(self) -> Inventory:
            return self.__session._get_inventory(
                DELETED_INVENTORY_PATH, filter_by_user=False
            )

        @property
        def inventory(self) -> Inventory:
            return self.saved_inventory + self.deleted_inventory

        @property
        def saved_equipment(self) -> Equipment:
            return self.saved_inventory.apply(lambda item: item.get_equipment())

        @property
        def deleted_equipment(self) -> Equipment:
            return self.deleted_inventory.apply(lambda item: item.get_equipment())

        @property
        def approved_changelog(self) -> Changelog:
            return self.__session._get_changelog(
                APPROVED_CHANGE_CONTROL_PATH, "APPROVED", filter_by_user=False
            )

        @property
        def rejected_changelog(self) -> Changelog:
            return self.__session._get_changelog(
                REJECTED_CHANGE_CONTROL_PATH, "REJECTED", filter_by_user=False
            )

        @property
        def changelog(self) -> Changelog:
            return self.approved_changelog + self.rejected_changelog

    class Current:
        def __init__(self, session: Session, shared: Session.Shared):
            self.__session = session
            self.__shared = shared

        @property
        def user(self) -> User:
            return self.__session._Session__user

        @property
        def credentials(self) -> Credentials:
            node = self.__shared.credentials_list.find_if(
                lambda credentials: credentials.get_user_id() == self.user.get_id()
            )

            if node is None:
                raise RuntimeError(f"User with ID {self.user.get_id()} not found.")

            return node.get_data()

        @property
        def add_requests(self) -> RequestList:
            return self.__session._get_requests(
                ADD_REQUESTS_PATH, "PENDING", "agregar", filter_by_user=True
            )

        @property
        def delete_requests(self) -> RequestList:
            return self.__session._get_requests(
                DELETE_REQUESTS_PATH, "PENDING", "eliminar", filter_by_user=True
            )

        @property
        def pending_requests(self) -> RequestList:
            return self.add_requests + self.delete_requests

        @property
        def approved_requests(self) -> RequestList:
            return self.approved_changelog.apply(lambda entry: entry.get_request())

        @property
        def rejected_requests(self) -> RequestList:
            return self.rejected_changelog.apply(lambda entry: entry.get_request())

        @property
        def non_pending_requests(self) -> RequestList:
            return self.approved_requests + self.rejected_requests

        @property
        def requests(self) -> RequestList:
            return self.pending_requests + self.non_pending_requests

        @property
        def saved_inventory(self) -> Inventory:
            return self.__session._get_inventory(
                SAVED_INVENTORY_PATH, filter_by_user=True
            )

        @property
        def deleted_inventory(self) -> Inventory:
            return self.__session._get_inventory(
                DELETED_INVENTORY_PATH, filter_by_user=True
            )

        @property
        def inventory(self) -> Inventory:
            return self.saved_inventory + self.deleted_inventory

        @property
        def saved_equipment(self) -> EquipmentList:
            return EquipmentList(self.saved_inventory.apply(lambda item: item.get_equipment()))

        @property
        def deleted_equipment(self) -> EquipmentList:
            return EquipmentList(self.deleted_inventory.apply(lambda item: item.get_equipment()))

        @property
        def approved_changelog(self) -> Changelog:
            return self.__session._get_changelog(
                APPROVED_CHANGE_CONTROL_PATH, "APPROVED", filter_by_user=True
            )

        @property
        def rejected_changelog(self) -> Changelog:
            return self.__session._get_changelog(
                REJECTED_CHANGE_CONTROL_PATH, "REJECTED", filter_by_user=True
            )

        @property
        def changelog(self) -> Changelog:
            return self.approved_changelog + self.rejected_changelog

    def _get_requests(
        self,
        path: Path,
        status: Literal["PENDING", "APPROVED", "REJECTED"],
        action: Literal["agregar", "eliminar"],
        filter_by_user: bool,
    ) -> RequestList:
        request_list = RequestList(filename=path)

        if path.exists():
           request_list.load_from_file() 

        if filter_by_user:
            request_list = request_list.filter_if(
                lambda request: request.get_user_id() == self.__user.get_id()
            )

        request_list.set_status(status)
        request_list.set_action(action)
        return request_list

    def _get_inventory(self, path: Path, filter_by_user: bool) -> Inventory:
        inventory = Inventory(filename=path)
        
        if path.exists():
            inventory.load_from_file()

        if filter_by_user:
            inventory = inventory.filter_if(
                lambda item: True
            )

        return inventory

    def _get_changelog(
        self,
        path: Path,
        status: Literal["PENDING", "APPROVED", "REJECTED"],
        filter_by_user: bool,
    ) -> Changelog:
        changelog = Changelog(filename=path)

        if path.exists():
            changelog.load_from_file()
        
        if filter_by_user:
            changelog = changelog.filter_if(
                lambda entry: entry.get_user_id() == self.__user.get_id()
            )

        changelog.set_status(status)
        return changelog
