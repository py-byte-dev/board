from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import FSInputFile, Message
from dishka.integrations.aiogram import FromDishka

from backend.application import interfaces
from backend.config import Config
from backend.domain.templates.menu_texts import main_menu_text

router = Router()


@router.message(CommandStart())
async def process_bot_launch(
    message: Message,
    config: FromDishka[Config],
    kb_builder: FromDishka[interfaces.KeyboardBuilder],
):
    await message.answer_photo(
        photo=FSInputFile(
            path=config.banner.file_path,
            filename='banner.jpg',
        ),
        caption=main_menu_text(),
        reply_markup=kb_builder.get_main_menu_kb().as_markup(),
    )
