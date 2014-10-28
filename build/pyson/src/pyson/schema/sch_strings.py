from propertylib.properties import default_property
from pyson.schema.schema_class import Schema
from pyson.schema.util import get_schemas, from_simple
from pyson.schema import errors
from pyson.types import is_string
import re

class Str(Schema):
    '''
    Examples
    --------
    
    >>> Str().is_valid('Forty two')
    True
    >>> Str().is_valid(42)
    False
    >>> Str(max_length=5).is_valid('Forty two')
    False
    '''

    INFO_ATTRIBUTES = Schema.INFO_ATTRIBUTES + [ 'max_length' ]
    NULL = u''

    @from_simple
    def validate(self, obj):
        if is_string(obj):
            if self.max_length is None:
                return True
            else:
                return self.max_length >= len(obj)
        else:
            return False

    @classmethod
    def obj_from_string(cls, obj):
        return obj

    max_length = default_property(None)

    def adapt(self, obj, inplace=False, path=[]):
        if self.is_valid(obj):
            return unicode(obj)
        else:
            raise errors.AdaptationError((None, path))

class Text(Str):
    pass

class Regex(Str):
    def __init__(self, regex, *args, **kwds):
        if isinstance(regex, basestring):
            self.regex = re.compile(regex)
        else:
            self.regex = regex
        super(Regex, self).__init__(*args, **kwds)

    @from_simple
    def validate(self, obj):
        super(Regex, self).validate(obj)
        return self.regex.match(obj) is not None

class Email(Regex):
    '''
    Example
    -------
    
    >>> Email().is_valid('foo@bar.com')
    True
    >>> Email().is_valid('foo_bar')
    False
    '''

    email_re = re.compile('^[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+$')
    def __init__(self, *args, **kwds):
        super(Email, self).__init__(self.email_re, *args, **kwds)

class Lang(Regex):
    '''
    Example
    -------
    
    >>> Lang().is_valid('pt-br')
    True
    >>> Lang().is_valid('pt')
    True
    >>> Lang().is_valid('portuguese')
    False
    '''

    lang_re = re.compile('^[a-z][a-z](-[a-z][a-z])?$')
    def __init__(self, *args, **kwds):
        super(Lang, self).__init__(self.lang_re, *args, **kwds)


__all__ = get_schemas(globals())
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
