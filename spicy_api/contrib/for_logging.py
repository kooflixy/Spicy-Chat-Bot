import logging
import time

logger = logging.getLogger('spicy')

def do_log(func):
    async def wrapped(*args, **kwargs):
        if args[0]._logs:
            lkwargs = kwargs
            if 'message' in kwargs:
                lkwargs['message'] = lkwargs['message'][:50]
            start_time = time.time()
            logger.info(f'Func {func.__name__} started args: {lkwargs}')

        res = await func(*args, **kwargs)
        
        if args[0]._logs:
            busy_time = time.time() - start_time
            logger.info(f'Func {func.__name__} completed in {busy_time} s args: {lkwargs}')
        return res
    return wrapped