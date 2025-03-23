from collections.abc import Collection
from dataclasses import dataclass
from uuid import UUID

from backend.domain.entities.category import Category
from backend.domain.entities.city import City
from backend.domain.entities.media import MediaType
from backend.domain.entities.store_resource import StoreResource


@dataclass(slots=True)
class Store:
    id: UUID
    title: str
    description: str
    preview_media_type: MediaType
    main_media_type: MediaType
    main_page_url: str
    display_priority: int


@dataclass(slots=True)
class StoreDetails:
    store: Store
    cities: Collection[City]
    categories: Collection[Category]
    resources: Collection[StoreResource]
