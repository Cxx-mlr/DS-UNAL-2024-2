from __future__ import annotations

from typing_extensions import (
    TypeVar,
    Protocol,
    runtime_checkable,
)


T = TypeVar("T", bound="CSVSerializable")


@runtime_checkable
class CSVSerializable(Protocol):
    def to_csv(self) -> str: ...

    @classmethod
    def from_csv(cls: type[T], csv_string: str) -> T: ...
