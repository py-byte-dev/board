from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class StoreCity:
    id: UUID
    store_id: UUID
    city_id: UUID
