from aiogram.fsm.state import State, StatesGroup


class AddCity(StatesGroup):
    titles = State()


class AddCategory(StatesGroup):
    titles = State()


class AddStore(StatesGroup):
    title = State()
    description = State()
    cities = State()
    categories = State()
    main_url = State()
    resources_url = State()
    preview_media_pc = State()
    preview_media_mobile = State()
    main_media_pc = State()
    main_media_mobile = State()
    priority = State()


class ChangeStore(StatesGroup):
    title = State()
    description = State()
    display_priority = State()
    main_page_url = State()
    resources_url = State()
    preview_media_pc = State()
    preview_media_mobile = State()
    main_media_pc = State()
    main_media_mobile = State()


class AddBanner(StatesGroup):
    target_url = State()
    pc_media = State()
    mobile_media = State()
    display_priority = State()


class ChangeBanner(StatesGroup):
    target_url = State()
    pc_media = State()
    mobile_media = State()
    display_priority = State()
