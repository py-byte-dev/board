import argparse
import logging
from collections.abc import Callable, Coroutine
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dishka import AsyncContainer, make_async_container
from dishka.integrations import aiogram as aiogram_integration, fastapi as fastapi_integration
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from backend import ioc
from backend.config import Config
from backend.presentation.api.routers import router
from backend.presentation.bot.handlers import router_list
from backend.presentation.bot.middlewares.user_access import UserAcessMiddleware
from backend.presentation.exceptions_mapping import EXCEPTIONS_MAPPING

config = Config()


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f'{config.webhook.url}{config.webhook.path}', allowed_updates=['message', 'callback_query'])


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')


def create_bot(token: str) -> Bot:
    return Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )


def create_dispatcher(routers: list[Router], container: AsyncContainer) -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers)
    dp.startup.register(on_startup)

    middleware = UserAcessMiddleware(container=container)
    dp.message.outer_middleware(middleware)
    dp.callback_query.outer_middleware(middleware)

    return dp


def create_bot_app(dp: Dispatcher, bot: Bot) -> web.Application:
    app = web.Application()

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(
        app,
        path=config.webhook.path,
    )
    setup_application(app, dp, bot=bot)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_api_app(
        router: APIRouter,
        container: AsyncContainer,
        exc_mapping: dict[
            int | type[Exception],
            Callable[[Request, Any], Coroutine[Any, Any, Response]],
        ],
):
    app = FastAPI(lifespan=lifespan, exception_handlers=exc_mapping, openapi_url="/api/openapi.json", docs_url="/api/docs")
    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    fastapi_integration.setup_dishka(container, app)
    return app


def launch_bot(bot: Bot, container: AsyncContainer, routers: list[Router]):
    setup_logging()

    dp = create_dispatcher(routers, container)
    aiogram_integration.setup_dishka(container=container, router=dp, auto_inject=True)
    app = create_bot_app(dp, bot)

    web.run_app(app, host=config.webhook.host, port=config.webhook.port)


def launch_api(
        container: AsyncContainer,
        router: APIRouter,
        exc_mapping: dict[
            int | type[Exception],
            Callable[[Request, Any], Coroutine[Any, Any, Response]],
        ],
):
    setup_logging()
    uvicorn.run(
        create_api_app(
            container=container,
            router=router,
            exc_mapping=exc_mapping,
        ),
        host=config.api.host,
        port=config.api.port,
        lifespan='on',
    )


def main():
    parser = argparse.ArgumentParser(
        description='Launch API or Telegram bot.',
    )

    parser.add_argument(
        '--app',
        type=str,
        default='bot',
        help='Specifies the type of application to run. Options are "api" or "bot". The default value is "bot".',
    )

    args = parser.parse_args()

    if args.app == 'bot':
        bot = create_bot(token=config.bot.token)
        bot_container = make_async_container(
            ioc.ApplicationProvider(),
            ioc.InfrastructureProvider(),
            aiogram_integration.AiogramProvider(),
            context={Config: config, Bot: bot},
        )
        launch_bot(bot=bot, container=bot_container, routers=router_list)

    elif args.app == 'api':
        api_container = make_async_container(
            ioc.ApplicationProvider(),
            ioc.InfrastructureProvider(),
            context={Config: config},
        )
        launch_api(container=api_container, router=router, exc_mapping=EXCEPTIONS_MAPPING)


if __name__ == '__main__':
    main()
