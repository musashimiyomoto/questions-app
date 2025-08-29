import redis.asyncio as redis

from settings import auth_settings, redis_settings

redis_client = redis.StrictRedis(
    host=redis_settings.host,
    port=redis_settings.port,
    db=redis_settings.db,
    decode_responses=True,
)


async def set_verify_code(identifier: str, code: str) -> None:
    """Set the code to the redis client.

    Args:
        identifier: The identifier.
        code: The code.

    """
    await redis_client.setex(
        name=identifier, time=auth_settings.verify_code_ttl, value=code
    )


async def get_verify_code(identifier: str) -> str | None:
    """Get the code from the redis client.

    Args:
        identifier: The identifier.

    Returns:
        The code.

    """
    return await redis_client.get(name=identifier)
