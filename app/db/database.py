import ssl
from urllib.parse import urlparse

from tortoise import Tortoise

from app.core.config import settings


def get_db_config():
    db_url = settings.DATABASE_URL
    
    # URL 파싱
    parsed = urlparse(db_url)
    
    # SSL 컨텍스트
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    return {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": parsed.hostname,
                    "port": parsed.port or 5432,
                    "user": parsed.username,
                    "password": parsed.password,
                    "database": parsed.path.lstrip("/"),
                    "ssl": ssl_ctx,
                },
            },
        },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            },
        },
    }


TORTOISE_ORM = get_db_config()


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()