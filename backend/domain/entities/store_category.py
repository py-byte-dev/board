from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class StoreCategory:
    id: UUID
    store_id: UUID
    category_id: UUID
