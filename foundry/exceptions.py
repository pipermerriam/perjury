class UniqueValueTimeoutError(RuntimeError):
    """
    Raised when a generator hangs for too long while trying to return a unique value.
    """
    pass
