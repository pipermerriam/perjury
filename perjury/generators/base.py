from perjury import util


class BaseGenerator(object):
    """
    Base class for all foundry generator classes.
    """
    depth_limit = 50
    unique = True
    key_fn = None
    seen = None

    def __init__(self):
        if self.unique:
            self.generator = util.unique(
                    fn=self.generator,
                    depth_limit=self.depth_limit,
                    key_fn=self.key_fn,
                    seen=self.seen,
                    )

    def __call__(self):
        return self.generator()

    def generator(self):
        raise NotImplementedError('Generator classes must implement their own'
                ' `generator` method.')
