from backend.domain.entities.category import Category
from backend.domain.entities.city import City
from backend.domain.entities.store import Store, StoreDetails
from backend.domain.entities.store_resource import StoreResource


class StoreMapper:
    @staticmethod
    def result_to_store_details(result: dict) -> StoreDetails:
        return StoreDetails(
            store=Store(
                id=result['store_id'],
                title=result['store_title'],
                description=result['description'],
                preview_media_type=result['preview_media_type'],
                main_media_type=result['main_media_type'],
                main_page_url=result['main_page_url'],
                display_priority=result['display_priority'],
            ),
            cities=[
                City(
                    id=city['id'],
                    title=city['title'],
                )
                for city in result['cities']
            ],
            categories=[
                Category(
                    id=category['id'],
                    title=category['title'],
                )
                for category in result['categories']
            ],
            resources=[
                StoreResource(
                    id=resource['id'],
                    title=resource['title'],
                    target_url=resource['target_url'],
                    store_id=resource['store_id'],
                )
                for resource in result['resources']
            ],
        )
