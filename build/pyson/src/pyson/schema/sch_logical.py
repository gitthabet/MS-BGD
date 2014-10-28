from pyson.schema.schema_class import Schema
from pyson.schema.util import get_schemas
from pyson.schema import errors

class Logical(Schema):
    INFO_ATTRIBUTES = Schema.INFO_ATTRIBUTES + [ '_schemas' ]

    def __init__(self, *args, **kwds):
        super(Logical, self).__init__(**kwds)
        self._schemas = []
        map(self.add, [sch for sch in args])

    def add(self, schema):
        '''Add a schema to the list of _schemas.'''

        cls = type(self)
        schema = self.as_schema(schema)
        if isinstance(schema, cls):
            self._schemas.extend(schema._schemas)
        else:
            self._schemas.append(schema)
        if not hasattr(self, 'default'):
            try:
                self.default = schema.default
            except AttributeError:
                pass

    def adapt(self, obj, inplace=False, path=[]):
        partial = None
        for v in self._schemas:
            try:
                return v.adapt(obj, inplace, path)
            except errors.PartialAdaptationError as ex:
                partial = ex
            except errors.AdaptationError:
                pass
        if partial is not None:
            raise partial
        else:
            raise errors.AdaptationError((None, path))

class AND(Logical):
    '''
    Logical **and** or between two _schemas.
    
    Examples
    --------
    
    >>> from pyson.schema import *
    >>> AND(Int(), Cte(42)).is_valid(42)
    True
    >>> (Int() & Cte(42)).is_valid(12)
    False
    '''

    name = '<and>'

    def validate(self, obj, lazy=True, path=[]):
        for v in self._schemas:
            if not v.is_valid(obj, lazy=True):
                msg = "%s object is not a valid '%s'" % (type(obj), type(v).__name__)
                raise errors.ValidationError((msg, path))


class OR(Logical):
    '''
    Logical **or** between two _schemas.
    
    Examples
    --------
    
    >>> from pyson.schema import *
    >>> OR(Int(), Real()).is_valid(42)
    True
    >>> (Int() | Str()).is_valid(42.0)
    False
    '''

    def validate(self, obj, lazy=True, path=[]):
        partial = None
        for v in self._schemas:
            try:
                v.validate(obj, lazy, path)
            except errors.PartialValidationError as ex:
                partial = ex
            except errors.ValidationError:
                pass
            else:
                return
        if partial is not None:
            raise partial
        else:
            v_json_types = ', '.join(set(type(v).__name__ for v in self._schemas))
            msg = "%%(path)s is none of: '%s'" % v_json_types
            raise errors.ValidationError((msg, path))

# Save specialized _schemas into the Schema class
Schema.OR_SCHEMA = OR
Schema.AND_SCHEMA = AND

__all__ = get_schemas(globals())
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
