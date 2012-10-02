from perjury.exceptions import UniqueValueTimeoutError


def unique(fn, depth_limit=50, key_fn=None, seen=None):
    """
    Decorator that ensures a function only ever returns unique values.  You can
    override the ``depth_limit`` to define the max number of recursions before
    failing.  Make sure that ``depth_limit`` is never long that the value
    returned from ``sys.getrecursionlimit``.
    """
    if seen is None:
        seen = set()

    if key_fn is None:
        key_fn = lambda x: x

    def wrapper():
        for _ in xrange(depth_limit):
            ret = fn()
            key = key_fn(ret)

            if key not in seen:
                seen.add(key)
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
