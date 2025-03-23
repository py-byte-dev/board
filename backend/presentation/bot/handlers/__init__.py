from backend.presentation.bot.handlers.callback import router as callback_router
from backend.presentation.bot.handlers.common import router as common_router
from backend.presentation.bot.handlers.message import router as message_router

router_list = [
    common_router,
    message_router,
    callback_router,
]

__all__ = ['router_list']
