from uuid import UUID

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import FromDishka

from backend.application import interfaces
from backend.application.use_cases.banner import (
    DeleteBannerInteractor,
    GetBannerInteractor,
    GetBannersInteractor,
    SaveBannerInteractor,
)
from backend.application.use_cases.category import (
    DeleteCategoryInteractor,
    GetAllCategoriesInteractor,
    GetStoreCategoriesInteractor,
)
from backend.application.use_cases.city import DeleteCityInteractor, GetAllCitiesInteractor, GetStoreCitiesInteractor
from backend.application.use_cases.store import (
    CanAddStoreInteractor,
    DeleteStoreInteractor,
    GetAllStoresInteractor,
    GetStoreDetailsInteractor,
    GetStoreInteractor,
    SaveStoreInteractor,
)
from backend.application.use_cases.store_category import AddStoreCategoryInteractor, DeleteStoreCategoryInteractor
from backend.application.use_cases.store_city import AddStoreCityInteractor, DeleteStoreCityInteractor
from backend.application.use_cases.store_resource import DeleteStoreResourceInteractor, GetStoreResourcesInteractor
from backend.config import Config
from backend.domain import exceptions as domain_exceptions
from backend.domain.templates.exceptions_text import (
    no_baners_for_edit_error_text,
    no_categories_for_add_store_error_text,
    no_categories_for_delete_error_text,
    no_cities_for_add_store_error_text,
    no_cities_for_delete_error_text,
    no_stores_for_edit_error_text,
    pagination_error_text,
    store_not_found_by_id_error_text,
    unchosen_categories_error_text,
    unchosen_cities_error_text,
)
from backend.domain.templates.menu_texts import (
    add_banner_menu_text,
    add_store_menu_text,
    banner_details_text,
    choice_banner_for_edit_menu_text,
    choice_store_for_edit_menu_text,
    get_banner_edit_menu_text,
    get_category_for_delete_menu_text,
    get_category_title_menu_text,
    get_city_for_delete_menu_text,
    get_city_title_menu_text,
    get_store_edit_menu_text,
    main_menu_text,
    select_action_menu_text,
    store_city_selection_menu_text,
    store_details_menu_text,
    success_store_save_text,
    success_banner_save_text
)
from backend.infrastructure.services.bot.helpers.items_displayer import ItemsDisplayer
from backend.presentation.bot.states.user import AddBanner, AddCategory, AddCity, AddStore, ChangeBanner, ChangeStore

router = Router()


@router.callback_query(F.data == 'main_menu')
async def display_main_menu(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    await call.message.edit_caption(caption=main_menu_text(), reply_markup=kb_builder.get_main_menu_kb().as_markup())


@router.callback_query(F.data == 'cities_menu')
async def display_cities_menu(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_cities_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'add_city')
async def get_city_title(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_caption(
        caption=get_city_title_menu_text(),
        reply_markup=kb_builder.get_cities_return_kb().as_markup(),
    )
    await state.update_data(msg=msg)
    await state.set_state(AddCity.titles)


@router.callback_query(F.data == 'delete_cities_menu')
async def display_delete_cities_menu(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetAllCitiesInteractor],
):
    try:
        cities = await interactor()
        await call.answer()
        await call.message.edit_caption(
            caption=get_city_for_delete_menu_text(),
            reply_markup=kb_builder.get_cities_delete_menu_kb(cities=cities).as_markup(),
        )

    except domain_exceptions.CitiesNotFoundError:
        await call.answer(no_cities_for_delete_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('drop_city'))
async def process_drop_city(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteCityInteractor],
):
    _, city_id = call.data.split(':')

    try:
        cities = await interactor(city_id=city_id)
        await call.answer()
        caption = get_city_for_delete_menu_text()
        keyboard = kb_builder.get_cities_delete_menu_kb(cities=cities)
    except domain_exceptions.CitiesNotFoundError:
        caption = select_action_menu_text()
        keyboard = kb_builder.get_cities_menu_kb()

    await call.message.edit_caption(caption=caption, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == 'categories_menu')
async def display_categories_menu(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_categories_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'add_category')
async def get_category_title(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_caption(
        caption=get_category_title_menu_text(),
        reply_markup=kb_builder.get_categories_return_kb().as_markup(),
    )
    await state.update_data(msg=msg)
    await state.set_state(AddCategory.titles)


@router.callback_query(F.data == 'delete_categories_menu')
async def display_delete_categories_menu(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetAllCategoriesInteractor],
):
    try:
        categories = await interactor()
        await call.answer()
        await call.message.edit_caption(
            caption=get_category_for_delete_menu_text(),
            reply_markup=kb_builder.get_categories_delete_menu_kb(categories=categories).as_markup(),
        )
    except domain_exceptions.CategoriesNotFoundError:
        await call.answer(no_categories_for_delete_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('drop_category'))
async def process_drop_category(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteCategoryInteractor],
):
    _, category_id = call.data.split(':')

    try:
        categories = await interactor(category_id=category_id)
        await call.answer()
        caption = get_city_for_delete_menu_text()
        keyboard = kb_builder.get_categories_delete_menu_kb(categories=categories)
    except domain_exceptions.CategoriesNotFoundError:
        caption = select_action_menu_text()
        keyboard = kb_builder.get_categories_menu_kb()

    await call.message.edit_caption(caption=caption, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == 'stores_menu')
async def display_stores_menu(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    await state.clear()

    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_stores_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'add_store')
async def get_store_title(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[CanAddStoreInteractor],
):
    try:
        await interactor()

        await call.answer()
        msg = await call.message.edit_caption(
            caption=add_store_menu_text(),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )
        await state.update_data(msg=msg)
        await state.set_state(AddStore.title)

    except domain_exceptions.CitiesNotFoundError:
        await call.answer(no_cities_for_add_store_error_text(), show_alert=True)
    except domain_exceptions.CategoriesNotFoundError:
        await call.answer(no_categories_for_add_store_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('choice_city'))
async def process_choice_city(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    _, city_id = call.data.split(':')
    city_id = UUID(city_id)

    state_data = await state.get_data()
    chosen_cities = state_data.get('chosen_cities', {})
    cities = state_data['cities']

    if city_id in chosen_cities.keys():
        del chosen_cities[city_id]
    else:
        chosen_cities[city_id] = next(city.title for city in cities if city.id == city_id)

    await call.message.edit_caption(
        caption=add_store_menu_text(
            title=state_data['title'],
            description=state_data['description'],
            cities=chosen_cities.values(),
            step_iteration=3,
        ),
        reply_markup=kb_builder.get_cities_choice_menu_kb(cities=cities).as_markup(),
    )
    await state.update_data(chosen_cities=chosen_cities)


@router.callback_query(F.data == 'stop_cities_choice')
async def get_store_categories(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetAllCategoriesInteractor],
):
    state_data = await state.get_data()

    if not state_data.get('chosen_cities', None):
        return await call.answer(unchosen_cities_error_text(), show_alert=True)

    categories = await interactor()

    await call.message.edit_caption(
        caption=add_store_menu_text(
            title=state_data['title'],
            description=state_data['description'],
            cities=state_data['chosen_cities'].values(),
            step_iteration=4,
        ),
        reply_markup=kb_builder.get_categories_choice_menu_kb(categories=categories).as_markup(),
    )
    await state.update_data(cities=None, categories=categories)


@router.callback_query(F.data.startswith('choice_category'))
async def process_choice_category(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    _, category_id = call.data.split(':')
    category_id = UUID(category_id)

    state_data = await state.get_data()
    chosen_categories = state_data.get('chosen_categories', {})
    categories = state_data['categories']

    if category_id in chosen_categories.keys():
        del chosen_categories[category_id]
    else:
        chosen_categories[category_id] = next(category.title for category in categories if category.id == category_id)

    await call.message.edit_caption(
        caption=add_store_menu_text(
            title=state_data['title'],
            description=state_data['description'],
            cities=state_data['chosen_cities'].values(),
            categories=chosen_categories.values(),
            step_iteration=4,
        ),
        reply_markup=kb_builder.get_categories_choice_menu_kb(categories=categories).as_markup(),
    )
    await state.update_data(chosen_categories=chosen_categories)


@router.callback_query(F.data == 'stop_categories_choice')
async def get_store_main_url(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    state_data = await state.get_data()

    if not state_data.get('chosen_categories', None):
        return await call.answer(unchosen_categories_error_text(), show_alert=True)

    await call.message.edit_caption(
        caption=add_store_menu_text(
            title=state_data['title'],
            description=state_data['description'],
            cities=state_data['chosen_cities'].values(),
            categories=state_data['chosen_categories'].values(),
            step_iteration=5,
        ),
        reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
    )
    await state.update_data(categories=None)
    await state.set_state(AddStore.main_url)


@router.callback_query(F.data == 'save_store')
async def process_save_store(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[SaveStoreInteractor],
):
    state_data = await state.get_data()
    await state.clear()

    await interactor(
        title=state_data['title'],
        description=state_data['description'],
        cities=state_data['chosen_cities'].keys(),
        categories=state_data['chosen_categories'].keys(),
        main_page_url=state_data['main_url'],
        resources_url=state_data['resources_url'],
        preview_media_pc=state_data['preview_media_pc'],
        preview_media_mobile=state_data['preview_media_mobile'],
        main_media_pc=state_data['main_media_pc'],
        main_media_mobile=state_data['main_media_mobile'],
        display_priority=state_data['display_priority'],
    )
    await call.answer(success_store_save_text(), show_alert=True)
    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_stores_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'edit_stores_menu')
async def display_stores_for_edit(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetAllStoresInteractor],
):
    try:
        page, page_size = 1, 2
        stores = await interactor(page=page, page_size=page_size)
        total_pages = (stores.total + page_size - 1) // page_size

        await call.answer()
        await call.message.edit_caption(
            caption=choice_store_for_edit_menu_text(),
            reply_markup=kb_builder.get_stores_choice_menu_kb(
                paginated_items=stores, total_pages=total_pages, page=page
            ).as_markup(),
        )
        await state.update_data(page=page, page_size=page_size, total_pages=total_pages)
    except domain_exceptions.StoresNotFoundError:
        await call.answer(no_stores_for_edit_error_text(), show_alert=True)


@router.callback_query(F.data.in_({'prev_shops', 'next_shops'}))
async def display_paginate_shops(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetAllStoresInteractor],
        items_displayer: FromDishka[ItemsDisplayer],
):
    await items_displayer(
        call=call,
        state=state,
        kb_callback=kb_builder.get_stores_choice_menu_kb,
        interactor=interactor,
        caption_callback=choice_store_for_edit_menu_text,
        error_callback=pagination_error_text,
        kb_needs_items=True,
    )


@router.callback_query(F.data.startswith('store_details'))
async def display_store_details(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        config: FromDishka[Config],
        interactor: FromDishka[GetStoreDetailsInteractor],
):
    _, store_id = call.data.split(':')
    try:
        details = await interactor(store_id=store_id)
        await call.answer()
        await call.message.edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )
    except domain_exceptions.StoreNotFoundByIdError:
        await call.answer(store_not_found_by_id_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('store_cities_menu'))
async def display_store_cities(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetStoreCitiesInteractor],
):
    _, store_id = call.data.split(':')
    cities = await interactor(store_id=store_id)

    await call.message.edit_caption(
        caption=store_city_selection_menu_text(),
        reply_markup=kb_builder.get_store_cities_menu_kb(store_id=store_id, cities=cities).as_markup(),
    )
    await state.update_data(store_id=store_id)


@router.callback_query(F.data.startswith('link_city'))
async def add_store_city(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[AddStoreCityInteractor],
):
    _, city_id = call.data.split(':')
    state_data = await state.get_data()
    store_id = state_data['store_id']

    cities = await interactor(store_id=store_id, city_id=city_id)

    await call.message.edit_caption(
        caption=store_city_selection_menu_text(),
        reply_markup=kb_builder.get_store_cities_menu_kb(store_id=store_id, cities=cities).as_markup(),
    )


@router.callback_query(F.data.startswith('unlink_city'))
async def delete_store_city(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteStoreCityInteractor],
):
    _, city_id = call.data.split(':')
    state_data = await state.get_data()
    store_id = state_data['store_id']

    cities = await interactor(store_id=store_id, city_id=city_id)

    await call.message.edit_caption(
        caption=store_city_selection_menu_text(),
        reply_markup=kb_builder.get_store_cities_menu_kb(store_id=store_id, cities=cities).as_markup(),
    )


@router.callback_query(F.data.startswith('store_categories_menu'))
async def display_store_categories(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetStoreCategoriesInteractor],
):
    _, store_id = call.data.split(':')
    categories = await interactor(store_id=store_id)

    await call.message.edit_caption(
        caption=store_city_selection_menu_text(),
        reply_markup=kb_builder.get_store_categories_menu_kb(store_id=store_id, categories=categories).as_markup(),
    )
    await state.update_data(store_id=store_id)


@router.callback_query(F.data.startswith('link_category'))
async def add_store_category(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[AddStoreCategoryInteractor],
):
    _, category_id = call.data.split(':')
    state_data = await state.get_data()
    store_id = state_data['store_id']

    categories = await interactor(store_id=store_id, category_id=category_id)

    await call.message.edit_caption(
        caption=store_city_selection_menu_text(),
        reply_markup=kb_builder.get_store_categories_menu_kb(store_id=store_id, categories=categories).as_markup(),
    )


@router.callback_query(F.data.startswith('unlink_category'))
async def delete_store_category(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteStoreCategoryInteractor],
):
    _, category_id = call.data.split(':')
    state_data = await state.get_data()
    store_id = state_data['store_id']

    categories = await interactor(store_id=store_id, category_id=category_id)

    await call.message.edit_caption(
        caption=store_city_selection_menu_text(),
        reply_markup=kb_builder.get_store_categories_menu_kb(store_id=store_id, categories=categories).as_markup(),
    )


@router.callback_query(F.data.startswith('change_store_priority'))
async def get_new_store_priority(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    action, store_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=action),
        reply_markup=kb_builder.get_store_return_kb(store_id=store_id).as_markup(),
    )
    await state.update_data(store_id=store_id, msg=msg)
    await state.set_state(ChangeStore.display_priority)


@router.callback_query(F.data.startswith('display_store_description'))
async def get_new_store_description(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetStoreInteractor],
):
    _, store_id = call.data.split(':')
    try:
        store = await interactor(store_id=store_id)
        await call.message.answer(text=store.description)
    except domain_exceptions.StoreNotFoundByIdError:
        await call.answer(store_not_found_by_id_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('change_store_description'))
async def get_new_store_description(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    action, store_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=action),
        reply_markup=kb_builder.get_store_return_kb(store_id=store_id).as_markup(),
    )
    await state.update_data(store_id=store_id, msg=msg)
    await state.set_state(ChangeStore.description)


@router.callback_query(F.data.startswith('change_store_title'))
async def get_new_store_title(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    action, store_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=action),
        reply_markup=kb_builder.get_store_return_kb(store_id=store_id).as_markup(),
    )
    await state.update_data(store_id=store_id, msg=msg)
    await state.set_state(ChangeStore.title)


@router.callback_query(F.data.startswith('store_recources_menu'))
async def display_store_resources_menu(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetStoreResourcesInteractor],
):
    action, store_id = call.data.split(':')

    rosources = await interactor(store_id=store_id)
    await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=action),
        reply_markup=kb_builder.store_resources_menu_kb(store_id=store_id, resources=rosources).as_markup(),
    )
    await state.update_data(store_id=store_id, action=action)


@router.callback_query(F.data == 'add_store_resources')
async def get_new_store_resources(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    state_data = await state.get_data()
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=call.data),
        reply_markup=kb_builder.get_store_resources_return_menu_kb(store_id=state_data['store_id']).as_markup(),
    )
    await state.update_data(msg=msg)
    await state.set_state(ChangeStore.resources_url)


@router.callback_query(F.data.startswith('drop_resource'))
async def process_resource_drop(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteStoreResourceInteractor],
):
    await call.answer()
    _, resource_id = call.data.split(':')
    rosources = await interactor(resource_id=resource_id)
    state_data = await state.get_data()

    await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=state_data['action']),
        reply_markup=kb_builder.store_resources_menu_kb(
            store_id=state_data['store_id'],
            resources=rosources,
        ).as_markup(),
    )


@router.callback_query(F.data.startswith('change_store_main_page_url'))
async def get_new_store_main_page_url(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    action, store_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=action),
        reply_markup=kb_builder.get_store_return_kb(store_id=store_id).as_markup(),
    )
    await state.update_data(store_id=store_id, msg=msg)
    await state.set_state(ChangeStore.main_page_url)


@router.callback_query(F.data.startswith('change_preview_media_menu'))
async def display_preview_media_menu(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    _, store_id = call.data.split(':')

    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_change_preview_media_menu_kb(store_id=store_id).as_markup(),
    )
    await state.update_data(store_id=store_id)


@router.callback_query(F.data.startswith('change_main_media_menu'))
async def display_main_media_menu(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    _, store_id = call.data.split(':')

    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_change_preview_media_menu_kb(store_id=store_id).as_markup(),
    )
    await state.update_data(store_id=store_id)


@router.callback_query(F.data == 'change_media_preview_pc')
async def get_new_preview_media_pc(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    state_data = await state.get_data()
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=call.data),
        reply_markup=kb_builder.get_store_return_kb(store_id=state_data['store_id']).as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(ChangeStore.preview_media_pc)


@router.callback_query(F.data == 'change_media_preview_mobile')
async def get_new_preview_media_mobile(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    state_data = await state.get_data()
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=call.data),
        reply_markup=kb_builder.get_store_return_kb(store_id=state_data['store_id']).as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(ChangeStore.preview_media_mobile)


@router.callback_query(F.data == 'change_media_main_pc')
async def get_new_main_media_pc(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    state_data = await state.get_data()
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=call.data),
        reply_markup=kb_builder.get_store_return_kb(store_id=state_data['store_id']).as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(ChangeStore.main_media_pc)


@router.callback_query(F.data == 'change_media_main_mobile')
async def get_new_main_media_mobile(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    state_data = await state.get_data()
    msg = await call.message.edit_caption(
        caption=get_store_edit_menu_text(action=call.data),
        reply_markup=kb_builder.get_store_return_kb(store_id=state_data['store_id']).as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(ChangeStore.main_media_mobile)


@router.callback_query(F.data.startswith('drop_store'))
async def proccess_drop_store(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteStoreInteractor],
):
    await call.answer()
    _, store_id = call.data.split(':')
    try:
        state_data = await state.get_data()
        page = 1
        stores = await interactor(store_id=store_id, page=page, page_size=state_data['page_size'])
        total_pages = (stores.total + state_data['page_size'] - 1) // state_data['page_size']

        caption = choice_store_for_edit_menu_text()
        keyboard = kb_builder.get_stores_choice_menu_kb(paginated_items=stores, total_pages=total_pages, page=page)
        await state.update_data(total_pages=total_pages, page=page)
    except domain_exceptions.StoresNotFoundError:
        caption = select_action_menu_text()
        keyboard = kb_builder.get_stores_menu_kb()

    await call.message.edit_caption(caption=caption, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == 'banners_menu')
async def display_banners_menu(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    await state.clear()
    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_banners_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'add_banner')
async def get_banner_target_url(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_caption(
        caption=add_banner_menu_text(),
        reply_markup=kb_builder.get_banners_return_menu_kb().as_markup(),
    )
    await state.update_data(msg=msg)
    await state.set_state(AddBanner.target_url)


@router.callback_query(F.data == 'save_banner')
async def process_save_banner(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[SaveBannerInteractor],
):
    state_data = await state.get_data()
    await state.clear()

    await interactor(
        target_url=state_data['target_url'],
        pc_media=state_data['pc_media'],
        mobile_media=state_data['mobile_media'],
        display_priority=state_data['display_priority']
    )

    await call.answer(success_banner_save_text(), show_alert=True)
    await call.message.edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_banners_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'edit_banners_menu')
async def display_banners_for_edit(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetBannersInteractor],
):
    try:
        banners = await interactor()
        await call.answer()
        await call.message.edit_caption(
            caption=choice_banner_for_edit_menu_text(),
            reply_markup=kb_builder.get_banners_choice_menu(banners=banners).as_markup(),
        )
    except domain_exceptions.BannersNotFoundError:
        await call.answer(no_baners_for_edit_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('banner_details'))
async def display_banner_details(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetBannerInteractor],
        config: FromDishka[Config],
):
    _, banner_id = call.data.split(':')
    try:
        banner = await interactor(banner_id=banner_id)
        await call.answer()
        await call.message.edit_caption(
            caption=banner_details_text(banner=banner, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_banner_edit_menu_kb(banner_id=banner_id, display_priority=banner.display_priority).as_markup(),
        )
    except domain_exceptions.BannerNotFoundByIdError:
        pass


@router.callback_query(F.data.startswith('change_banner_url'))
async def get_new_banner_url(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()

    action, banner_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_banner_edit_menu_text(action=action),
        reply_markup=kb_builder.get_banner_return_kb(banner_id=banner_id).as_markup(),
    )

    await state.update_data(msg=msg, banner_id=banner_id)
    await state.set_state(ChangeBanner.target_url)


@router.callback_query(F.data.startswith('change_banner_pc'))
async def get_new_pc_banner(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()

    action, banner_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_banner_edit_menu_text(action=action),
        reply_markup=kb_builder.get_banner_return_kb(banner_id=banner_id).as_markup(),
    )

    await state.update_data(msg=msg, banner_id=banner_id)
    await state.set_state(ChangeBanner.pc_media)


@router.callback_query(F.data.startswith('change_banner_mobile'))
async def get_new_mobile_banner(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()

    action, banner_id = call.data.split(':')
    msg = await call.message.edit_caption(
        caption=get_banner_edit_menu_text(action=action),
        reply_markup=kb_builder.get_banner_return_kb(banner_id=banner_id).as_markup(),
    )

    await state.update_data(msg=msg, banner_id=banner_id)
    await state.set_state(ChangeBanner.mobile_media)


@router.callback_query(F.data.startswith('change_banner_priority'))
async def get_new_display_priority_banner(
        call: CallbackQuery,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await call.answer()
    action, banner_id = call.data.split(':')

    msg = await call.message.edit_caption(caption=get_banner_edit_menu_text(action=action),
                                          reply_markup=kb_builder.get_banner_return_kb(banner_id=banner_id).as_markup(), )
    await state.update_data(msg=msg, banner_id=banner_id)
    await state.set_state(ChangeBanner.display_priority)


@router.callback_query(F.data.startswith('drop_banner'))
async def proccess_drop_banner(
        call: CallbackQuery,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[DeleteBannerInteractor],
):
    await call.answer()
    _, banner_id = call.data.split(':')

    try:
        banners = await interactor(banner_id=banner_id)
        caption = choice_banner_for_edit_menu_text()
        keyboard = kb_builder.get_banners_choice_menu(banners=banners)
    except domain_exceptions.BannersNotFoundError:
        caption = select_action_menu_text()
        keyboard = kb_builder.get_banners_menu_kb()

    await call.message.edit_caption(caption=caption, reply_markup=keyboard.as_markup())
