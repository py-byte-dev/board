from dataclasses import dataclass
from uuid import UUID

from backend.domain.entities.media import MediaType


@dataclass(slots=True)
class Banner:
    id: UUID
    media_type: MediaType
    target_url: str
    display_priority: int
