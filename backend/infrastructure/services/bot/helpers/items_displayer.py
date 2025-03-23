from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


class ItemsDisplayer:
    async def __call__(
        self,
        call: CallbackQuery,
        state: FSMContext,
        kb_callback: callable,
        interactor: callable,
        caption_callback: callable,
        error_callback: callable,
        interactor_args: dict | None = None,
        caption_needs_items: bool = False,
        kb_needs_items: bool = False,
    ):
        interactor_args = interactor_args or {}

        state_data = await state.get_data()

        required_keys = ['page', 'page_size', 'total_pages']
        if not state_data or not all(key in state_data for key in required_keys):
            return await call.answer(error_callback(), show_alert=True)

        await call.answer()

        page, page_size, total_pages = (
            state_data['page'],
            state_data['page_size'],
            state_data['total_pages'],
        )

        if call.data.startswith('prev'):
            page = total_pages if page == 1 else page - 1
        elif call.data.startswith('next'):
            page = 1 if page == total_pages else page + 1

        interactor_args.update({'page': page, 'page_size': page_size})

        paginated_items = await interactor(**interactor_args)

        caption = caption_callback(paginated_items) if caption_needs_items else caption_callback()

        keyboard = (
            kb_callback(paginated_items, total_pages=total_pages, page=page)
            if kb_needs_items
            else kb_callback(
                total_pages=total_pages,
                page=page,
            )
        )

        await call.message.edit_caption(caption=caption, reply_markup=keyboard.as_markup())

        await state.update_data(page=page)
