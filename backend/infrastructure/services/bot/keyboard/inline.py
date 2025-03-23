from collections.abc import Collection
from uuid import UUID

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend.application import interfaces
from backend.domain.entities.banner import Banner
from backend.domain.entities.category import Category, CategorySelection
from backend.domain.entities.city import City, CitySelection
from backend.domain.entities.pagination import Pagination
from backend.domain.entities.store import Store
from backend.domain.entities.store_resource import StoreResource


class KeyboardBuilder(interfaces.KeyboardBuilder):
    def __init__(self):
        self._kb_builder: InlineKeyboardBuilder | None = None

    def get_main_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🌇 Города', callback_data='cities_menu')
        self._kb_builder.button(text='🛍 Категории', callback_data='categories_menu')
        self._kb_builder.button(text='🏪 Магазины', callback_data='stores_menu')
        self._kb_builder.button(text='🌌 Банера', callback_data='banners_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_cities_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='➕ Добавить', callback_data='add_city')
        self._kb_builder.button(text='➖ Удалить', callback_data='delete_cities_menu')
        self._kb_builder.button(text='⬅️ Назад', callback_data='main_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_cities_delete_menu_kb(self, cities=Collection[City]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for city in cities:
            self._kb_builder.button(text=f'{city.title}', callback_data=f'drop_city:{city.id}')

        self._kb_builder.button(text='⬅️ Назад', callback_data='cities_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_cities_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data='cities_menu')

        return self._kb_builder

    def get_categories_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='➕ Добавить', callback_data='add_category')
        self._kb_builder.button(text='➖ Удалить', callback_data='delete_categories_menu')
        self._kb_builder.button(text='⬅️ Назад', callback_data='main_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_categories_delete_menu_kb(self, categories=Collection[Category]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for category in categories:
            self._kb_builder.button(text=f'{category.title}', callback_data=f'drop_category:{category.id}')

        self._kb_builder.button(text='⬅️ Назад', callback_data='categories_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_categories_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data='categories_menu')

        return self._kb_builder

    def get_stores_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='➕ Добавить', callback_data='add_store')
        self._kb_builder.button(text='⚙️ Изменить', callback_data='edit_stores_menu')
        self._kb_builder.button(text='⬅️ Назад', callback_data='main_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_cities_choice_menu_kb(self, cities: Collection[City]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()
        for city in cities:
            self._kb_builder.button(text=f'{city.title}', callback_data=f'choice_city:{city.id}')

        self._kb_builder.adjust(2)

        self._kb_builder.row(
            InlineKeyboardButton(text='⬅️ Назад', callback_data='stores_menu'),
            InlineKeyboardButton(text='Дальше ➡️', callback_data='stop_cities_choice'),
        )

        return self._kb_builder

    def get_categories_choice_menu_kb(self, categories: Collection[Category]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()
        for category in categories:
            self._kb_builder.button(text=f'{category.title}', callback_data=f'choice_category:{category.id}')

        self._kb_builder.adjust(2)

        self._kb_builder.row(
            InlineKeyboardButton(text='⬅️ Назад', callback_data='stores_menu'),
            InlineKeyboardButton(text='Дальше ➡️', callback_data='stop_categories_choice'),
        )

        return self._kb_builder

    def get_stores_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data='stores_menu')

        return self._kb_builder

    def get_store_save_actions_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='✅ Да', callback_data='save_store')
        self._kb_builder.button(text='❌ Нет', callback_data='stores_menu')

        return self._kb_builder

    def get_stores_choice_menu_kb(
            self, paginated_items: Pagination[Store], total_pages: int, page: int
    ) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for store in paginated_items.items:
            self._kb_builder.button(
                text=f'{store.title} [{store.display_priority}]',
                callback_data=f'store_details:{store.id}',
            )
        self._kb_builder.adjust(1)

        if total_pages > 1:
            self._kb_builder.row(
                InlineKeyboardButton(text='⬅️', callback_data='prev_shops'),
                InlineKeyboardButton(text=f'[{page}/{total_pages}]', callback_data='current_page'),
                InlineKeyboardButton(text='➡️', callback_data='next_shops'),
            )

        self._kb_builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='stores_menu'))

        return self._kb_builder

    def get_store_edit_menu_kb(self, store_id: UUID, display_priority: int) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.row(
            InlineKeyboardButton(text='🌇 Города', callback_data=f'store_cities_menu:{store_id}'),
            InlineKeyboardButton(text='🛍 Категории', callback_data=f'store_categories_menu:{store_id}'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(
                text=f'📊 Приоритет [{display_priority}]',
                callback_data=f'change_store_priority:{store_id}',
            ),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='👀 Описание', callback_data=f'display_store_description:{store_id}'),
            InlineKeyboardButton(text='📃 Описание', callback_data=f'change_store_description:{store_id}'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='📌 Название', callback_data=f'change_store_title:{store_id}'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='🔗 Ресурс', callback_data=f'change_store_main_page_url:{store_id}'),
            InlineKeyboardButton(text='🔗 Доп.ресурсы', callback_data=f'store_recources_menu:{store_id}'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='🏞 Превью', callback_data=f'change_preview_media_menu:{store_id}'),
            InlineKeyboardButton(text='🌁 Баннер', callback_data=f'change_main_media_menu:{store_id}'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='🗑 Удалить', callback_data=f'drop_store:{store_id}'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='⬅️ Назад', callback_data='edit_stores_menu'),
        )

        return self._kb_builder

    def get_store_return_kb(self, store_id: UUID) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data=f'store_details:{store_id}')

        return self._kb_builder

    def get_store_cities_menu_kb(self, store_id: UUID, cities: Collection[CitySelection]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for city in cities:
            self._kb_builder.button(
                text=f'{city.title} [{"✅" if city.is_linked else "❌"}]',
                callback_data=f'{"unlink_city" if city.is_linked else "link_city"}:{city.id}',
            )
        self._kb_builder.adjust(2)
        self._kb_builder.row(
            InlineKeyboardButton(text='⬅️ Назад', callback_data=f'store_details:{store_id}'),
        )

        return self._kb_builder

    def get_store_categories_menu_kb(
            self,
            store_id: UUID,
            categories: Collection[CategorySelection],
    ) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for categories in categories:
            self._kb_builder.button(
                text=f'{categories.title} [{"✅" if categories.is_linked else "❌"}]',
                callback_data=f'{"unlink_category" if categories.is_linked else "link_category"}:{categories.id}',
            )
        self._kb_builder.adjust(2)
        self._kb_builder.row(
            InlineKeyboardButton(text='⬅️ Назад', callback_data=f'store_details:{store_id}'),
        )

        return self._kb_builder

    def store_resources_menu_kb(self, store_id: UUID, resources: Collection[StoreResource]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for resource in resources:
            self._kb_builder.button(
                text=f'{resource.target_url[0:10]}...-{resource.title}',
                callback_data=f'drop_resource:{resource.id}',
            )

        self._kb_builder.button(text='➕ Добавить', callback_data='add_store_resources')
        self._kb_builder.button(text='⬅️ Назад', callback_data=f'store_details:{store_id}')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_store_resources_return_menu_kb(self, store_id: UUID) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data=f'store_recources_menu:{store_id}')

        return self._kb_builder

    def get_change_preview_media_menu_kb(self, store_id: UUID) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🌌 PC', callback_data='change_media_preview_pc')
        self._kb_builder.button(text='🌌 Mobile', callback_data='change_media_preview_mobile')
        self._kb_builder.button(text='⬅️ Назад', callback_data=f'store_details:{store_id}')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_change_main_media_menu_kb(self, store_id: UUID) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🌌 PC', callback_data='change_media_main_pc')
        self._kb_builder.button(text='🌌 Mobile', callback_data='change_media_main_mobile')
        self._kb_builder.button(text='⬅️ Назад', callback_data=f'store_details:{store_id}')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_banners_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='➕ Добавить', callback_data='add_banner')
        self._kb_builder.button(text='️⚙️ Изменить', callback_data='edit_banners_menu')
        self._kb_builder.button(text='⬅️ Назад', callback_data='main_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_banners_choice_menu(self, banners: Collection[Banner]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for banner in banners:
            self._kb_builder.button(text=f'{banner.target_url}', callback_data=f'banner_details:{banner.id}')

        self._kb_builder.button(text='⬅️ Назад', callback_data='main_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_banners_return_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data='main_menu')

        return self._kb_builder

    def get_banner_save_actions_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='✅ Да', callback_data='save_banner')
        self._kb_builder.button(text='❌ Нет', callback_data='banners_menu')

        return self._kb_builder

    def get_banner_edit_menu_kb(self, banner_id: UUID, display_priority: int) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🌌 Банер [PC]', callback_data=f'change_banner_pc:{banner_id}')
        self._kb_builder.button(text='🌌 Банер [MOBILE]', callback_data=f'change_banner_mobile:{banner_id}')
        self._kb_builder.button(text='🔗 Ресурс', callback_data=f'change_banner_url:{banner_id}')
        self._kb_builder.button(text=f'📊 Приоритет [{display_priority}]', callback_data=f'change_banner_priority:{banner_id}')
        self._kb_builder.button(text='🗑 Удалить', callback_data=f'drop_banner:{banner_id}')
        self._kb_builder.button(text='⬅️ Назад', callback_data='banners_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_banner_return_kb(self, banner_id: UUID) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⬅️ Назад', callback_data=f'banner_details:{banner_id}')

        return self._kb_builder
