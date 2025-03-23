from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class City:
    id: UUID
    title: str


@dataclass(slots=True)
class CitySelection:
    id: UUID
    title: str
    is_linked: bool
