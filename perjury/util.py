from perjury.exceptions import UniqueValueTimeoutError


def unique(fn, depth_limit=50):
    """
    Decorator that ensures a function only ever returns unique values.  You can
    override the ``depth_limit`` to define the max number of recursions before
    failing.  Make sure that ``depth_limit`` is never long that the value
    returned from ``sys.getrecursionlimit``.
    """
    seen = set()

    def wrapper():
        for _ in xrange(depth_limit):
            ret = fn()

            if ret not in seen:
                seen.add(ret)
                return ret

        raise UniqueValueTimeoutError

    return wrapper


def forever(fn):
    """
    Returns an iterable that will call the function passed in until forever.
    """
    while True:
        yield fn()


def times(fn, times):
    """
    Returns an iterable that will call the function only the specified number
    of times.
    """
    for i in xrange(times):
        yield fn()
