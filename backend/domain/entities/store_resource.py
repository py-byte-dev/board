from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class StoreResource:
    id: UUID
    title: str
    target_url: str
    store_id: UUID
