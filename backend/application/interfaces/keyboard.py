from abc import abstractmethod
from collections.abc import Collection
from typing import Any, Protocol
from uuid import UUID

from backend.domain.entities.banner import Banner
from backend.domain.entities.category import Category, CategorySelection
from backend.domain.entities.city import City, CitySelection
from backend.domain.entities.pagination import Pagination
from backend.domain.entities.store import Store
from backend.domain.entities.store_resource import StoreResource


class Keyboard(Protocol):
    def as_markup(self) -> Any: ...


class KeyboardBuilder(Protocol):
    @abstractmethod
    def get_main_menu_kb(self) -> Keyboard: ...

    # @abstractmethod
    # def get_main_menu_return_kb(self) -> Keyboard: ...
    #
    @abstractmethod
    def get_cities_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_cities_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_cities_delete_menu_kb(self, cities: Collection[City]) -> Keyboard: ...

    @abstractmethod
    def get_categories_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_categories_delete_menu_kb(self, categories: Collection[Category]) -> Keyboard: ...

    @abstractmethod
    def get_categories_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_stores_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_cities_choice_menu_kb(self, cities: Collection[City]) -> Keyboard: ...

    @abstractmethod
    def get_categories_choice_menu_kb(self, categories: Collection[Category]) -> Keyboard: ...

    @abstractmethod
    def get_stores_menu_return_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_store_save_actions_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_stores_choice_menu_kb(
            self, paginated_items: Pagination[Store], total_pages: int, page: int
    ) -> Keyboard: ...

    @abstractmethod
    def get_store_edit_menu_kb(self, store_id: UUID, display_priority: int) -> Keyboard: ...

    @abstractmethod
    def get_store_return_kb(self, store_id: UUID) -> Keyboard: ...

    @abstractmethod
    def get_store_cities_menu_kb(self, store_id: UUID, cities: Collection[CitySelection]) -> Keyboard: ...

    @abstractmethod
    def get_store_categories_menu_kb(self, store_id: UUID, categories: Collection[CategorySelection]) -> Keyboard: ...

    @abstractmethod
    def store_resources_menu_kb(self, store_id: UUID, resources: Collection[StoreResource]) -> Keyboard: ...

    @abstractmethod
    def get_store_resources_return_menu_kb(self, store_id: UUID) -> Keyboard: ...

    @abstractmethod
    def get_change_preview_media_menu_kb(self, store_id: UUID) -> Keyboard: ...

    @abstractmethod
    def get_change_main_media_menu_kb(self, store_id: UUID) -> Keyboard: ...

    @abstractmethod
    def get_banners_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_banners_choice_menu(self, banners: Collection[Banner]) -> Keyboard: ...

    @abstractmethod
    def get_banners_return_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_banner_save_actions_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_banner_edit_menu_kb(self, banner_id: UUID, display_priority: int) -> Keyboard: ...

    @abstractmethod
    def get_banner_return_kb(self, banner_id: UUID) -> Keyboard: ...
