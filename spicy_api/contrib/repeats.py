import asyncio
import logging

from spicy_api import settings

logger = logging.getLogger(__name__)


def async_retry(async_function):
    """This function tries to repeat an asynchronous function again
    if an error occurred during its execution."""

    async def wrapped(*args, **kwargs):
        try:
            return await async_function(*args, **kwargs)
        except Exception as ex:
            logger.error(f"{async_function.__name__} had problems with: \"{ex}\"")
            
            for attempt in range(1, settings.RETRY_MAX_COUNT+1):
                await asyncio.sleep(settings.RETRY_TIMEOUT)
                
                try:
                    data = await async_function(*args, **kwargs)
                    logger.info(f"{async_function.__name__} was successfully retried at {attempt} time")
                    return data
                except Exception as wrap_ex:
                    logger.error(f"{async_function.__name__} was retried at {attempt} time: \"{wrap_ex}\", func had {args=} and {kwargs=}")
    return wrapped