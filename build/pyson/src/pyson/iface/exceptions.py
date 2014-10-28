class _DummyDefault(object):
    def __new__(cls):
        try:
            return cls.singleton
        except:
            cls.singleton = object.__new__(cls)
            return cls.singleton

    def __str__(self):
        return 'DEFAULT'

    def __repr__(self):
        return 'DEFAULT'

    def __unicode__(self):
        return u'DEFAULT'

DEFAULT = _DummyDefault()

class IndexKeyError(KeyError, IndexError):
    pass
