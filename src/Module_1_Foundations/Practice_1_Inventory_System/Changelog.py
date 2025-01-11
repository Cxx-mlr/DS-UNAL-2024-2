from ChangelogEntry import ChangelogEntry
from FileBackedList import FileBackedList

from typing_extensions import Literal


class Changelog(FileBackedList[ChangelogEntry]):
    T = ChangelogEntry

    def set_action(self, action: Literal["agregar", "eliminar"]):
        self.for_each(lambda entry: entry.set_action(action))

    def set_status(self, status: Literal["PENDING", "APPROVED", "REJECTED"]):
        self.for_each(lambda entry: entry.set_status(status))
