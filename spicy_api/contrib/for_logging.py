import logging
import time

logger = logging.getLogger('spicy')

def do_log(func):
    async def wrapped(*args, **kwargs):
        self = args[0]
        if self._logs:
            lkwargs = kwargs
            if 'message' in kwargs:
                lkwargs['message'] = lkwargs['message'][:50]
            start_time = time.time()

        res = await func(*args, **kwargs)
        
        if self._logs:
            busy_time = time.time() - start_time
            logger.info(f'{self.__class__.__name__}.{func.__name__} completed in {busy_time} s args: {lkwargs}')
        return res
    return wrapped