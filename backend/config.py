from dataclasses import dataclass, field
from os import environ as env


@dataclass(slots=True)
class PgConfig:
    db: str = field(default_factory=lambda: env.get('POSTGRES_DB').strip())
    host: str = field(default_factory=lambda: env.get('POSTGRES_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('POSTGRES_PORT').strip()))
    user: str = field(default_factory=lambda: env.get('POSTGRES_USER').strip())
    password: str = field(default_factory=lambda: env.get('POSTGRES_PASSWORD').strip())

    def create_connection_string(self) -> str:
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


@dataclass(slots=True)
class RedisConfig:
    host: str = field(default_factory=lambda: env.get('REDIS_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('REDIS_PORT').strip()))
    db: str = field(default_factory=lambda: env.get('REDIS_DB').strip())

    def create_connection_string(self) -> str:
        return f'redis://{self.host}:{self.port}/{self.db}'


@dataclass(slots=True)
class MinioConfig:
    user: str = field(default_factory=lambda: env.get('MINIO_ROOT_USER').strip())
    password: str = field(default_factory=lambda: env.get('MINIO_ROOT_PASSWORD').strip())
    url: str = field(default_factory=lambda: env.get('MINIO_URL').strip())
    bucket: str = field(default_factory=lambda: env.get('MINIO_BUCKET').strip())


@dataclass
class TgBotConfig:
    token: str = field(default_factory=lambda: env.get('TG_BOT_TOKEN').strip())
    admins: list[int] = field(default_factory=lambda: list(map(int, env.get('ADMINS').strip().split(','))))


@dataclass
class WebHookConfig:
    host: str = field(default_factory=lambda: env.get('WEBHOOK_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('WEBHOOK_PORT').strip()))
    url: str = field(default_factory=lambda: env.get('WEBHOOK_URL').strip())
    path: str = field(default_factory=lambda: env.get('WEBHOOK_PATH').strip())


@dataclass
class ApiConfig:
    host: str = field(default_factory=lambda: env.get('API_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('API_PORT').strip()))


@dataclass
class BannerConfig:
    file_path: str = field(default_factory=lambda: env.get('BANNER_PATH').strip())


@dataclass(slots=True)
class Config:
    pg: PgConfig = field(default_factory=PgConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    minio: MinioConfig = field(default_factory=MinioConfig)
    bot: TgBotConfig = field(default_factory=TgBotConfig)
    webhook: WebHookConfig = field(default_factory=WebHookConfig)
    api: ApiConfig = field(default_factory=ApiConfig)
    banner: BannerConfig = field(default_factory=BannerConfig)
