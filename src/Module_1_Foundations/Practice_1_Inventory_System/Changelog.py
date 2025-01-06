from __future__ import annotations

from ChangelogEntry import ChangelogEntry

from typing_extensions import List, Optional, Callable


from config import READ_PATH, WRITE_PATH

class Changelog:
    def __init__(self, capacity: int = 100) -> Changelog:
        self.__capacity: int = capacity

        self.__entry_list: List[Optional[ChangelogEntry]] = [None for _ in range(self.__capacity)]
        self.__entry_count: int = 0

    def add(self, entry: ChangelogEntry) -> Optional[ChangelogEntry]:
        if self.__entry_count >= self.__capacity:
            return None
        
        for index, entry_i in enumerate(self.__entry_list):
            if entry_i is None:
                self.__entry_list[index] = entry
                break

        self.__entry_count += 1
        return entry

    def delete(self, pred: Callable[[ChangelogEntry], bool]) -> Optional[ChangelogEntry]:
        if (index := self.index(pred)) == -1:
            return None

        deleted = self.__entry_list[index]
        self.__entry_list[index] = None
        for next_index in range(index + 1, self.__entry_count):
            self.__entry_list[next_index - 1] = self.__entry_list[next_index]
            self.__entry_list[next_index] = None
        
        self.__entry_count -= 1
        return deleted

    def find(self, pred: Callable[[ChangelogEntry], bool]) -> Optional[ChangelogEntry]:
        for entry in self:
            if pred(entry):
                return entry
        return -1
    
    def index(self, pred: Callable[[ChangelogEntry], bool]) -> int:
        for index, changelog_entry in enumerate(self):
            if pred(changelog_entry):
                return index
        return -1
    
    def filter(self, pred: Callable[[ChangelogEntry], bool]) -> Changelog:
        new_changelog = Changelog()

        for changelog_entry in self.__entry_list[:self.__entry_count]:
            if pred(changelog_entry):
                new_changelog.add(changelog_entry)

        return new_changelog
    
    def __getitem__(self, index: int) -> ChangelogEntry:
        return self.__entry_list[:self.__entry_count][index]
    
    def __iter__(self):
        return iter(self.__entry_list[:self.__entry_count])
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        return False

    def save_to_file(self, filename: str = "Control_de_cambios.txt"):
        data = "\n".join(entry.to_csv() for entry in self)
        with open(WRITE_PATH / filename, "wt", encoding="utf-8") as file:
            file.writelines(
                data
            )

    def load_from_file(self, filename: str = "Control_de_cambios.txt"):
        try:
            with open(READ_PATH / filename, "rt", encoding="utf-8") as file:
                for csv_string in file:
                    entry = ChangelogEntry.from_csv(csv_string)
                    self.add(entry)
        except FileNotFoundError:
            print("File not found. Failed to load data.")

    def __str__(self) -> str:
        return "\n".join(f"{entry}" for entry in self)