from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Category:
    id: UUID
    title: str


@dataclass(slots=True)
class CategorySelection:
    id: UUID
    title: str
    is_linked: bool
