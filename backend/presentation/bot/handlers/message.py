from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka

from backend.application import interfaces
from backend.application.use_cases.banner import (
    UpdateBannerUrlInteractor,
    UpdateMobileBannerInteractor,
    UpdatePcBannerInteractor,
    UpdateBannerDisplayPriorityInteractor
)
from backend.application.use_cases.category import SaveCategoriesInteractor
from backend.application.use_cases.city import GetAllCitiesInteractor, SaveCitiesInteractor
from backend.application.use_cases.store import (
    UpdateStoreDescriptionInteractor,
    UpdateStoreDisplayPriorityInteractor,
    UpdateStoreMainMediaMobileInteractor,
    UpdateStoreMainMediaPcInteractor,
    UpdateStoreMainPageUrlInteractor,
    UpdateStorePrevieMediaMobileInteractor,
    UpdateStorePrevieMediaPcInteractor,
    UpdateStoreTitleInteractor,
)
from backend.application.use_cases.store_resource import AddStoreResourcesInteractor
from backend.config import Config
from backend.domain.templates.menu_texts import (
    add_banner_menu_text,
    add_store_menu_text,
    banner_details_text,
    get_store_edit_menu_text,
    select_action_menu_text,
    store_details_menu_text,
)
from backend.infrastructure import exceptions as infra_exceptions
from backend.infrastructure.services.bot.media.media_service import MediaService
from backend.presentation.bot.states.user import AddBanner, AddCategory, AddCity, AddStore, ChangeBanner, ChangeStore

router = Router()


@router.message(AddCity.titles)
async def process_save_cities(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[SaveCitiesInteractor],
):
    await message.delete()
    await interactor(titles=message.text)

    state_data = await state.get_data()
    await state.clear()
    await state_data['msg'].edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_cities_menu_kb().as_markup(),
    )


@router.message(AddCategory.titles)
async def process_save_categories(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[SaveCategoriesInteractor],
):
    await message.delete()
    await interactor(titles=message.text)

    state_data = await state.get_data()
    await state.clear()
    await state_data['msg'].edit_caption(
        caption=select_action_menu_text(),
        reply_markup=kb_builder.get_categories_menu_kb().as_markup(),
    )


@router.message(AddStore.title)
async def get_store_description(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.delete()
    if len(message.text) <= 64:
        state_data = await state.get_data()

        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=message.text,
                step_iteration=2,
            ),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )

        await state.update_data(title=message.text)
        await state.set_state(AddStore.description)


@router.message(AddStore.description)
async def get_store_cities(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[GetAllCitiesInteractor],
):
    await message.delete()
    if len(message.text) <= 4096:
        state_data = await state.get_data()

        cities = await interactor()

        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=message.text,
                step_iteration=3,
            ),
            reply_markup=kb_builder.get_cities_choice_menu_kb(cities=cities).as_markup(),
        )

        await state.update_data(description=message.text, cities=cities)


@router.message(AddStore.main_url)
async def get_store_recources_url(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.delete()
    if 'http' in message.text and len(message.text) <= 512:
        state_data = await state.get_data()
        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=state_data['description'],
                cities=state_data['chosen_cities'].values(),
                categories=state_data['chosen_categories'].values(),
                main_url=message.text,
                step_iteration=6,
            ),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )
        await state.update_data(main_url=message.text)
        await state.set_state(AddStore.resources_url)


@router.message(AddStore.resources_url)
async def get_store_previe_media_pc(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.delete()

    for resource in message.text.strip().split('\n'):
        parts = resource.strip().split('|')
        if len(parts) != 2:
            return

        url = parts[0].strip()

        if not url.startswith(('http://', 'https://')) or len(url) > 512:
            return

    state_data = await state.get_data()
    await state_data['msg'].edit_caption(
        caption=add_store_menu_text(
            title=state_data['title'],
            description=state_data['description'],
            cities=state_data['chosen_cities'].values(),
            categories=state_data['chosen_categories'].values(),
            main_url=state_data['main_url'],
            resources_url=message.text,
            step_iteration=7,
        ),
        reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
    )
    await state.update_data(resources_url=message.text)
    await state.set_state(AddStore.preview_media_pc)


@router.message(AddStore.preview_media_pc)
async def get_store_previe_media_mobile(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)

        state_data = await state.get_data()
        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=state_data['description'],
                cities=state_data['chosen_cities'].values(),
                categories=state_data['chosen_categories'].values(),
                main_url=state_data['main_url'],
                resources_url=state_data['resources_url'],
                preview_media_pc=media,
                step_iteration=8,
            ),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )
        await state.update_data(preview_media_pc=media)
        await state.set_state(AddStore.preview_media_mobile)

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddStore.preview_media_mobile)
async def get_store_main_media_pc(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)

        state_data = await state.get_data()
        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=state_data['description'],
                cities=state_data['chosen_cities'].values(),
                categories=state_data['chosen_categories'].values(),
                main_url=state_data['main_url'],
                resources_url=state_data['resources_url'],
                preview_media_pc=state_data['preview_media_pc'],
                preview_media_mobile=media,
                step_iteration=9,
            ),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )
        await state.update_data(preview_media_mobile=media)
        await state.set_state(AddStore.main_media_pc)

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddStore.main_media_pc)
async def get_store_main_media_mobile(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)

        state_data = await state.get_data()
        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=state_data['description'],
                cities=state_data['chosen_cities'].values(),
                categories=state_data['chosen_categories'].values(),
                main_url=state_data['main_url'],
                resources_url=state_data['resources_url'],
                preview_media_pc=state_data['preview_media_pc'],
                preview_media_mobile=state_data['preview_media_mobile'],
                main_media_pc=media,
                step_iteration=10,
            ),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )
        await state.update_data(main_media_pc=media)
        await state.set_state(AddStore.main_media_mobile)

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddStore.main_media_mobile)
async def get_save_action(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)

        state_data = await state.get_data()
        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=state_data['description'],
                cities=state_data['chosen_cities'].values(),
                categories=state_data['chosen_categories'].values(),
                main_url=state_data['main_url'],
                resources_url=state_data['resources_url'],
                preview_media_pc=state_data['preview_media_pc'],
                preview_media_mobile=state_data['preview_media_mobile'],
                main_media_pc=state_data['main_media_pc'],
                main_media_mobile=media,
                step_iteration=11,
            ),
            reply_markup=kb_builder.get_stores_menu_return_kb().as_markup(),
        )
        await state.update_data(main_media_mobile=media)
        await state.set_state(AddStore.priority)

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddStore.priority)
async def get_save_action(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.delete()
    if message.text.isdigit():
        display_priority = int(message.text)

        state_data = await state.get_data()
        await state_data['msg'].edit_caption(
            caption=add_store_menu_text(
                title=state_data['title'],
                description=state_data['description'],
                cities=state_data['chosen_cities'].values(),
                categories=state_data['chosen_categories'].values(),
                main_url=state_data['main_url'],
                resources_url=state_data['resources_url'],
                preview_media_pc=state_data['preview_media_pc'],
                preview_media_mobile=state_data['preview_media_mobile'],
                main_media_pc=state_data['main_media_pc'],
                main_media_mobile=state_data['main_media_mobile'],
                display_priority=display_priority,
                step_iteration=12,
            ),
            reply_markup=kb_builder.get_store_save_actions_kb().as_markup(),
        )
        await state.update_data(display_priority=display_priority)


@router.message(ChangeStore.display_priority)
async def process_update_store_display_priority(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[UpdateStoreDisplayPriorityInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    if message.text.isdigit():
        state_data = await state.get_data()
        await state.clear()

        display_priority = int(message.text)
        details = await interactor(store_id=state_data['store_id'], display_priority=display_priority)

        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )


@router.message(ChangeStore.description)
async def process_update_store_description(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[UpdateStoreDescriptionInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    if len(message.text) <= 4096:
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], description=message.text)

        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )


@router.message(ChangeStore.title)
async def process_update_story_title(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[UpdateStoreTitleInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    if len(message.text) <= 64:
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], title=message.text)

        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )


@router.message(ChangeStore.main_page_url)
async def process_update_store_main_page(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[UpdateStoreMainPageUrlInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    if 'http' in message.text and len(message.text) <= 512:
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], main_page_url=message.text)

        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )


@router.message(ChangeStore.resources_url)
async def process_add_store_recources(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[AddStoreResourcesInteractor],
):
    await message.delete()
    for resource in message.text.strip().split('\n'):
        parts = resource.strip().split('|')
        if len(parts) != 2:
            return

        url = parts[0].strip()

        if not url.startswith(('http://', 'https://')) or len(url) > 512:
            return

    state_data = await state.get_data()

    rosources = await interactor(resources_url=message.text, store_id=state_data['store_id'])

    await state_data['msg'].edit_caption(
        caption=get_store_edit_menu_text(action=state_data['action']),
        reply_markup=kb_builder.store_resources_menu_kb(
            store_id=state_data['store_id'],
            resources=rosources,
        ).as_markup(),
    )


@router.message(ChangeStore.preview_media_pc)
async def process_update_preview_media_pc(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
        interactor: FromDishka[UpdateStorePrevieMediaPcInteractor],
        config: FromDishka[Config],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], media=media)
        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )
    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(ChangeStore.preview_media_mobile)
async def process_update_preview_media_mobile(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
        interactor: FromDishka[UpdateStorePrevieMediaMobileInteractor],
        config: FromDishka[Config],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], media=media)
        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )
    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(ChangeStore.main_media_pc)
async def process_update_main_media_pc(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
        interactor: FromDishka[UpdateStoreMainMediaPcInteractor],
        config: FromDishka[Config],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], media=media)
        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )
    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(ChangeStore.main_media_mobile)
async def process_update_main_media_pc(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
        interactor: FromDishka[UpdateStoreMainMediaMobileInteractor],
        config: FromDishka[Config],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()
        await state.clear()

        details = await interactor(store_id=state_data['store_id'], media=media)
        await state_data['msg'].edit_caption(
            caption=store_details_menu_text(details=details, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_store_edit_menu_kb(
                store_id=details.store.id,
                display_priority=details.store.display_priority,
            ).as_markup(),
        )
    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddBanner.target_url)
async def get_banner_pc_media(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.delete()
    url = message.text

    if not url.startswith(('http://', 'https://')) or len(url) > 512:
        return

    state_data = await state.get_data()

    await state_data['msg'].edit_caption(
        caption=add_banner_menu_text(targer_url=url, step_iteration=2),
        reply_markup=kb_builder.get_banners_return_menu_kb().as_markup(),
    )

    await state.update_data(target_url=url)
    await state.set_state(AddBanner.pc_media)


@router.message(AddBanner.pc_media)
async def get_banner_mobile_media(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()

        await state_data['msg'].edit_caption(
            caption=add_banner_menu_text(targer_url=state_data['target_url'], pc_media=media, step_iteration=3),
            reply_markup=kb_builder.get_banners_return_menu_kb().as_markup(),
        )

        await state.update_data(pc_media=media)
        await state.set_state(AddBanner.mobile_media)

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddBanner.mobile_media)
async def get_banner_display_priority(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
):
    await message.delete()

    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()

        await state_data['msg'].edit_caption(
            caption=add_banner_menu_text(
                targer_url=state_data['target_url'],
                pc_media=state_data['pc_media'],
                mobile_media=media,
                step_iteration=4,
            ),
            reply_markup=kb_builder.get_banners_return_menu_kb().as_markup(),
        )

        await state.update_data(mobile_media=media)
        await state.set_state(AddBanner.display_priority)

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(AddBanner.display_priority)
async def get_banner_save_action(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.delete()
    if message.text.isdigit():
        display_priority = int(message.text)
        state_data = await state.get_data()

        await state_data['msg'].edit_caption(
            caption=add_banner_menu_text(
                targer_url=state_data['target_url'],
                pc_media=state_data['pc_media'],
                mobile_media=state_data['mobile_media'],
                display_priority=display_priority,
                step_iteration=5,
            ),
            reply_markup=kb_builder.get_banner_save_actions_kb().as_markup(),
        )

        await state.update_data(display_priority=display_priority)


@router.message(ChangeBanner.target_url)
async def proccess_update_banner_target_url(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[UpdateBannerUrlInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    target_url = message.text
    if not target_url.startswith(('http://', 'https://')) or len(target_url) > 512:
        return
    state_data = await state.get_data()
    await state.clear()

    banner = await interactor(banner_id=state_data['banner_id'], target_url=target_url)

    await state_data['msg'].edit_caption(
        caption=banner_details_text(banner=banner, minio_url=config.minio.url, bucket=config.minio.bucket),
        reply_markup=kb_builder.get_banner_edit_menu_kb(banner_id=state_data['banner_id'],
                                                        display_priority=banner.display_priority).as_markup(),
    )


@router.message(ChangeBanner.pc_media)
async def process_update_banner_pc_media(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
        interactor: FromDishka[UpdatePcBannerInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()
        await state.clear()

        banner = await interactor(banner_id=state_data['banner_id'], media=media)

        await state_data['msg'].edit_caption(
            caption=banner_details_text(banner=banner, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_banner_edit_menu_kb(banner_id=state_data['banner_id'],
                                                            display_priority=banner.display_priority).as_markup(),
        )

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(ChangeBanner.mobile_media)
async def process_update_banner_mobile_media(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        media_service: FromDishka[MediaService],
        interactor: FromDishka[UpdateMobileBannerInteractor],
        config: FromDishka[Config],
):
    await message.delete()
    try:
        media = await media_service.download_media(message=message)
        state_data = await state.get_data()
        await state.clear()

        banner = await interactor(banner_id=state_data['banner_id'], media=media)

        await state_data['msg'].edit_caption(
            caption=banner_details_text(banner=banner, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_banner_edit_menu_kb(banner_id=state_data['banner_id'],
                                                            display_priority=banner.display_priority).as_markup(),
        )

    except infra_exceptions.InvalidMediaContentTypeError:
        pass


@router.message(ChangeBanner.display_priority)
async def process_update_banner_priority(
        message: Message,
        state: FSMContext,
        kb_builder: FromDishka[interfaces.KeyboardBuilder],
        interactor: FromDishka[UpdateBannerDisplayPriorityInteractor],
        config: FromDishka[Config]
):
    await message.delete()
    if message.text.isdigit():
        display_priority = int(message.text)
        state_data = await state.get_data()

        banner = await interactor(banner_id=state_data['banner_id'], display_priority=display_priority)

        await state_data['msg'].edit_caption(
            caption=banner_details_text(banner=banner, minio_url=config.minio.url, bucket=config.minio.bucket),
            reply_markup=kb_builder.get_banner_edit_menu_kb(banner_id=state_data['banner_id'],
                                                            display_priority=banner.display_priority).as_markup(),
        )

        await state.update_data(display_priority=display_priority)
