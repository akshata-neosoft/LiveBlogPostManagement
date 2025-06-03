import logging

# trace logger

trace_logger = logging.getLogger('trace_logger')


def trace_log(func):
    def decorator(*args, **kwargs):
        trace_logger.debug('Entering {0}:{1} with args={2}, kwargs={3}'.format(func.__module__, func.__name__, args,
                                                                               kwargs))
        # noinspection PyBroadException
        try:
            from rest_framework.request import Request
            if args[1] is not None and type(args[1]) == Request:
                trace_logger.debug("Request Body:{0}".format(args[1].data))
        except Exception:
            pass

        result = func(*args, **kwargs)
        trace_logger.debug('Response:{0}'.format(result))
        trace_logger.debug('Exiting {0}:{1}'.format(func.__module__, func.__name__))
        return result

    return decorator
