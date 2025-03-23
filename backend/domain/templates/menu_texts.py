from collections.abc import Iterable

from backend.domain.entities.banner import Banner
from backend.domain.entities.media import BannerMediaName, Media, StoreMediaName
from backend.domain.entities.store import StoreDetails


def main_menu_text() -> str:
    return '🌐 <b>Главное меню</b>'


def select_action_menu_text() -> str:
    return '📲 <b>Выберите действия:</b>'


def get_city_title_menu_text() -> str:
    return (
        '✍️ <b>Введит название города:\n\n</b>\n'
        'ℹ️ <i>Для множественного добавления введите название каждого города с новой строки</i>'
    )


def get_city_for_delete_menu_text() -> str:
    return '📲 <b>Выберите город для удаления:</b>'


def get_category_title_menu_text() -> str:
    return (
        '✍️ <b>Введит название категории:\n\n</b>\n'
        'ℹ️ <i>Для множественного добавления введите название каждой категории с новой строки</i>'
    )


def get_category_for_delete_menu_text() -> str:
    return '📲 <b>Выберите категорию для удаления:</b>'


def add_store_menu_text(
        title: str | None = None,
        description: str | None = None,
        cities: Iterable[str] | None = None,
        categories: Iterable[str] | None = None,
        main_url: str | None = None,
        resources_url: str | None = None,
        preview_media_pc: Media | None = None,
        preview_media_mobile: Media | None = None,
        main_media_pc: Media | None = None,
        main_media_mobile: Media | None = None,
        display_priority: int = 1,
        step_iteration: int = 1,
):
    step_mapping_texts = {
        1: '✍️ Введите название магазина (до 64 символов)',
        2: '✍️ Введите описание магазина (до 4096 символов)',
        3: '📍 Выберите города, в которых работает магазин:',
        4: '🛍 Выберите категории товаров магазина:',
        5: '🔗 Укажите основную ссылку на магазин:',
        6: '🔗 Добавьте дополнительные ссылки (формат: ссылка | заголовок) Для множественного добавления введите каждый ресурс с новой строки:',
        7: '📥 Отправьте превью медиа магазина для ПК (изображение/GIF):',
        8: '📥 Отправьте превью медиа магазина для телефона (изображение/GIF):',
        9: '📥 Отправьте основное медиа магазина для ПК (изображение/GIF):',
        10: '📥 Отправьте основное медиа магазина для телефона (изображение/GIF):',
        11: '✍️ Укажите приоритет магазина. Чем выше приоритет, тем выше позиция на борде.',
        12: '📲 Готово! Добавляем магазин на борд?',
    }

    return (
        '<b>🆕 Добавление нового магазина:</b>\n\n'
        f'▫️ <i>Название:</i> {title if title else "❌"}\n'
        f'▫️ <i>Описание:</i> {f"<b>{len(description)}/4096</b>" if description else "❌"}\n'
        f'▫️ <i>Города:</i> {",".join(cities) if cities else "❌"}\n'
        f'▫️ <i>Категории:</i> {",".join(categories) if categories else "❌"}\n'
        f'▫️ <i>Основной ресурс:</i> {main_url if main_url else "❌"}\n'
        f'▫️ <i>Доп. ресурсы:</i> <code>[{resources_url if resources_url else "❌"}]</code>\n'
        f'▫️ <i>Превью медиа PC:</i> {"✅" if preview_media_pc else "❌"}\n'
        f'▫️ <i>Превью медиа MOBILE:</i> {"✅" if preview_media_mobile else "❌"}\n'
        f'▫️ <i>Основное медиа PC:</i> {"✅" if main_media_pc else "❌"}\n'
        f'▫️ <i>Основное медиа MOBILE:</i> {"✅" if main_media_mobile else "❌"}\n'
        f'▫️ <i>Приоритет:</i> <b>{display_priority}</b>\n\n'
        f'<b>{step_mapping_texts[step_iteration]}</b>'
    )


def success_store_save_text() -> str:
    return '✅ Стор усшно сохранен:'


def choice_store_for_edit_menu_text() -> str:
    return '📲 <b>Выберите магазин для изменения:</b>'


def store_details_menu_text(details: StoreDetails, minio_url: str, bucket: str) -> str:
    resources_text = ''.join(f"• <a href='{res.target_url}'>{res.title}</a>\n" for res in details.resources) or '—'

    return (
        f'📌 <b>Название:</b> {details.store.title}\n'
        f'✏️ <b>Описание:</b> {len(details.store.description)}/4096 символов\n'
        f'🏙 <b>Города:</b> {", ".join(city.title for city in details.cities) or "—"}\n'
        f'🗂 <b>Категории:</b> {", ".join(category.title for category in details.categories) or "—"}\n\n'
        f"🌐 <b>Основной ресурс:</b> <a href='{details.store.main_page_url}'>{details.store.main_page_url}</a>\n"
        f'📎 <b>Доп. ресурсы:</b>\n{resources_text}\n'
        f'🖼 <i>Превью медиа:</i>\n'
        f"• PC: <a href='https://{minio_url}/{bucket}/{details.store.id}-{StoreMediaName.PC_PREVIEW}.{details.store.preview_media_type}'>глянуть</a>\n"
        f"• Mobile: <a href='https://{minio_url}/{bucket}/{details.store.id}-{StoreMediaName.MOBILE_PREVIEW}.{details.store.preview_media_type}'>глянуть</a>\n\n"
        f'🏞 <i>Основное медиа:</i>\n'
        f"• PC: <a href='https://{minio_url}/{bucket}/{details.store.id}-{StoreMediaName.PC_MAIN}.{details.store.main_media_type}'>глянуть</a>\n"
        f"• Mobile: <a href='https://{minio_url}/{bucket}/{details.store.id}-{StoreMediaName.MOBILE_MAIN}.{details.store.main_media_type}'>глянуть</a>\n"
    )


def store_city_selection_menu_text() -> str:
    return '📲 <b>Чтобы добавить/удалить город просто нажмите на него:</b>'


def store_category_selection_menu_text() -> str:
    return '📲 <b>Чтобы добавить/удалить категорию просто нажмите на нее:</b>'


def get_store_edit_menu_text(action: str) -> str:
    step_edit_texts = {
        'change_store_title': '✍️ Введите <b>новое название</b> магазина (до 64 символов):',
        'change_store_description': '✍️ Введите <b>новое описание</b> магазина (до 4096 символов):',
        'change_store_main_page_url': '🔗 Укажите <b>новую основную ссылку</b> на магазин:',
        'store_recources_menu': 'ℹ️ Для удаления доп.ссылки просто нажмите на нее:',
        'add_store_resources': '🔗 Добавьте дополнительные ссылки (формат: ссылка | заголовок) Для множественного добавления введите каждый ресурс с новой строки:',
        'change_media_preview_pc': '📥 Отправьте <b>новое превью медиа</b> магазина для ПК (изображение/GIF):',
        'change_media_preview_mobile': '📥 Отправьте <b>новое превью медиа</b> магазина для телефона (изображение/GIF):',
        'change_media_main_pc': '📥 Отправьте <b>новое основное медиа</b> магазина для ПК (изображение/GIF):',
        'change_media_main_mobile': '📥 Отправьте <b>новое основное медиа</b> магазина для телефона (изображение/GIF):',
        'change_store_priority': '✍️ Укажите <b>новый приоритет</b> магазина. Чем выше приоритет, тем выше позиция на борде.',
    }

    return step_edit_texts[action]


def add_banner_menu_text(
        targer_url: str | None = None,
        pc_media: Media | None = None,
        mobile_media: Media | None = None,
        display_priority: int = 1,
        step_iteration: int = 1,
):
    step_mapping_texts = {
        1: '🔗 Укажите ссылку на ресурс:',
        2: '📥 Отправьте баннер для ПК (изображение/GIF):',
        3: '📥 Отправьте баннер для телефона (изображение/GIF):',
        4: '✍️ Укажите приоритет баннера. Чем выше приоритет, тем выше позиция на борде.',
        5: '📲 Готово! Добавляем баннер на борд?',
    }

    return (
        f'▫️<i>Ссылка на ресурс:</i> {targer_url if targer_url else "❌"}\n'
        f'▫️ <i>Баннер [PC]:</i> {"✅" if pc_media else "❌"}\n'
        f'▫️ <i>Баннер [Mobile]:</i> {"✅" if mobile_media else "❌"}\n'
        f'▫️ <i>Приоритет:</i> <b>{display_priority}</b>\n\n'
        f'<b>{step_mapping_texts[step_iteration]}</b>'
    )


def success_banner_save_text() -> str:
    return '✅ Баннер усшно сохранен:'


def choice_banner_for_edit_menu_text() -> str:
    return '📲 <b>Выберите баннер для изменения:</b>'


def banner_details_text(banner: Banner, minio_url: str, bucket: str) -> str:
    return (
        f"🌐 <b>Ресурс:</b> <a href='{banner.target_url}'>{banner.target_url}</a>\n\n"
        f'🖼 <i>Баннер:</i>\n'
        f"• PC: <a href='https://{minio_url}/{bucket}/{banner.id}-{BannerMediaName.PC}.{banner.media_type}'>глянуть</a>\n"
        f"• Mobile: <a href='https://{minio_url}/{bucket}/{banner.id}-{BannerMediaName.MOBILE}.{banner.media_type}'>глянуть</a>\n\n"
    )


def get_banner_edit_menu_text(action: str) -> str:
    step_edit_texts = {
        'change_banner_url': '🔗 Укажите <b>новую ссылку</b> на ресурс:',
        'change_banner_pc': '📥 Отправьте <b>новые баннер</b> для ПК (изображение/GIF):',
        'change_banner_mobile': '📥 Отправьте <b>новые баннер</b> для телефона (изображение/GIF):',
        'change_banner_priority': '✍️ Укажите <b>новый приоритет</b> баннера. Чем выше приоритет, тем выше позиция на борде.',
    }

    return step_edit_texts[action]
