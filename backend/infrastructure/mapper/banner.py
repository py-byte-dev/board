import json
from uuid import UUID

from backend.domain.entities.banner import Banner


class BannerMapper:
    @staticmethod
    def entity_to_json(banner: Banner) -> str:
        return json.dumps(
            {
                'id': str(banner.id),
                'media_type': banner.media_type,
                'target_url': banner.target_url,
                'display_priority': banner.display_priority
            },
        )

    @staticmethod
    def json_to_entity(json_str: str) -> Banner:
        parsed_dict = json.loads(json_str)
        return Banner(
            id=UUID(parsed_dict['id']),
            media_type=parsed_dict['media_type'],
            target_url=parsed_dict['target_url'],
            display_priority=parsed_dict['display_priority']
        )
