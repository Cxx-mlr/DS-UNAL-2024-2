from __future__ import annotations

from User import User

from Inventory import Inventory
from Changelog import Changelog
from Agenda import Agenda

from Credentials import Credentials
from CredentialsList import CredentialsList
import itertools

class Session:
    def __init__(self, user: User):
        self._user = user
    
    @property
    def _users(self) -> Agenda:
        users = Agenda()
        users.load_from_file(
            filename="Empleados.txt"
        )

        return users
    
    @property
    def _inventory(self) -> Inventory:
        inventory = Inventory()
        inventory.load_from_file(
            filename="InventarioGeneral.txt"
        )

        return inventory

    @property
    def _add_requests(self) -> Inventory:
        add_requests = Inventory()
        add_requests.load_from_file(
            filename="Solicitudes_agregar.txt"
        )

        return add_requests

    @property
    def _delete_requests(self) -> Inventory:
        delete_requests = Inventory()
        delete_requests.load_from_file(
            filename="Solicitudes_eliminar.txt"
        )

        return delete_requests
    
    @property
    def _requests(self) -> Inventory:
        requests = Inventory()

        for request in itertools.chain(self._add_requests, self._delete_requests):
            requests.add(request)

        return requests
    
    @property
    def _changelog(self) -> Changelog:
        changelog = Changelog()
        changelog.load_from_file(
            filename="Control_de_cambios.txt"
        )

        return changelog
    
    @property
    def _credentials_list(self) -> CredentialsList:
        credentials_list = CredentialsList()
        credentials_list.load_from_file(
            filename="Password.txt"
        )

        return credentials_list

    @property
    def _user_inventory(self) -> Inventory:
        return self._inventory.filter(
            lambda item: item.get_user_id() == self._user.get_id()
        )
    
    @property
    def _user_add_requests(self) -> Inventory:
        return self._add_requests.filter(
            lambda item: item.get_user_id() == self._user.get_id()
        )

    @property
    def _user_delete_requests(self) -> Inventory:
        return self._delete_requests.filter(
            lambda item: item.get_user_id() == self._user.get_id()
        )

    @property
    def _user_requests(self) -> Inventory:
        user_requests = Inventory()

        for request in itertools.chain(self._user_add_requests, self._user_delete_requests):
            user_requests.add(request)

        return user_requests

    @property
    def _user_changelog(self) -> Changelog:
        return self._changelog.filter(
            lambda entry: entry.get_user_id() == self._user.get_id()
        )
    
    @property
    def _user_credentials(self) -> Credentials:
        return self._credentials_list.filter(
            lambda credentials: credentials.get_user_id() == self._user.get_id()
        )[0]

    def get_username(self) -> str:
        return self._user.get_name()
    
    def get_role(self) -> str:
        return self._user_credentials.get_role()