from pyson.schema import errors
from pyson.schema.schema_class import Schema
from pyson.schema.util import get_schemas, from_simple
from pyson.types import is_integer, is_real, is_boolean, is_number

class Number(Schema):
    '''
    Examples
    --------
    
    >>> Number().is_valid(42.0)
    True
    >>> Number().is_valid(42)
    True
    >>> Number().is_valid('Forty two')
    False
    '''

    @from_simple
    def validate(self, obj):
        return is_number(obj)

    def adapt(self, obj, inplace=False, path=[]):
        if not self.is_valid(obj):
            try:
                return int(obj)
            except TypeError:
                try:
                    return float(obj)
                except:
                    raise errors.AdaptationError((None, path))
        else:
            return obj

class Int(Schema):
    '''
    Examples
    --------
    
    >>> Int().is_valid(42)
    True
    >>> Int().is_valid('Forty two')
    False
    '''
#    INFO_ATTRIBUTES = Schema.INFO_ATTRIBUTES + [ 'range' ]

    @from_simple
    def validate(self, obj):
        return is_integer(obj)

    def adapt(self, obj, inplace=False, path=[]):
        try:
            return int(obj)
        except TypeError:
            raise errors.AdaptationError((None, path))

class Real(Schema):
    '''
    Examples
    --------
    
    >>> Real().is_valid(42.0)
    True
    >>> Real().is_valid(42)
    False
    '''
    @from_simple
    def validate(self, obj):
        return is_real(obj)

    def adapt(self, obj, inplace=False, path=[]):
        try:
            return float(obj)
        except TypeError:
            raise self.AdaptationError((None, path))


class Bool(Schema):
    '''
    Validate boolean objects.
    
    Example
    -------
    
    >>> Bool().validate(True)
    >>> Bool().validate(0)
    Traceback (most recent call last):
    ...
    ValidationError: on key $: <type 'int'> object not a <Bool>
    '''

    @from_simple
    def validate(self, obj):
        return is_boolean(obj)

    @classmethod
    def obj_from_string(cls, obj):
        try:
            return { 'true': True, 'false': False }[obj.lower()]
        except KeyError:
            raise ValueError("invalid boolean: '%s'" % obj)

__all__ = get_schemas(globals())
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
