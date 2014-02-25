def fancy_import(name):
    """
    This takes a fully qualified object name, like 'accounts.models.ProxyUser'
    and turns it into the accounts.models.ProxyUser object.
    """
    import_path, import_me = name.rsplit('.', 1)
    imported = __import__(import_path, globals(), locals(), [import_me], -1)
    return getattr(imported, import_me)


class ResourceCheckMixin(object):
    resource_path = None
    iteration_count = 10000

    def setUp(self):
        super(ResourceCheckMixin, self).setUp()
        if self.resource_path is None:
            self.fail()
        try:
            self.resource = fancy_import(self.resource_path)
        except ImportError:
            self.fail('Could not import resource from `{0}`.'.format(
                self.resource_path
            ))

    def test_basic_generation(self):
        for i in xrange(self.iteration_count):
            self.resource()
