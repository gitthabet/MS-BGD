import functools
from pyson.schema import errors

def get_schemas(dic):
    'Return a list of all subtypes of the Schema type to feed to __all__'
    from pyson.schema.schema_class import Schema

    ret_lst = []
    for k, v in dic.items():
        if isinstance(v, type) and issubclass(v, Schema) and not k.startswith('_'):
            ret_lst.append(k)

    return ret_lst

def from_simple(*args, **kwds):
    '''Decorator that convert simple implementation of supported methods into a
    full-fledged implementation. A few methods are supported and their 
    description is given bellow:
    
    Schema.validate()
    -----------------
    
    The Schema.validate() method has a signature schema(obj, lazy=True, path=[])
    A simple Schema validator is a function of a single positional argument
    that returns ``True`` if argument is validated and ``False`` otherwise.
    
    Optionally, the function may raise a ValidationError to flag that the object
    is not valid. The exception will be re-raised adjusting its 'path' attribute. 
    
    Simple validators are more convenient to implement in subclasses
    
    >>> from pyson.schema import Schema
    >>> class Unicode(Schema):
    ...     @from_simple
    ...     def validate(self, obj):
    ...         return isinstance(obj, unicode)
    >>> Unicode().validate(u'one', lazy=True)
    >>> Unicode().validate('one', path=['foo', 'bar'])
    Traceback (most recent call last):
    ...
    ValidationError: on key $.foo.bar: <type 'str'> object not a <Unicode>
    '''

    if not args:
        return functools.partial(from_simple, **kwds)

    if not (len(args) == 1):
        raise TypeError("'from_simple' can be called with a single positional argument or only with keyword arguments")

    # Delegate decoration to specialized worker function
    func = args[0]
    worker_name = func.func_name + '_worker'

    try:
        worker_func = globals()[worker_name]
    except KeyError:
        name = func.func_name
        raise TypeError('simple functions not supported for %s() methods' % name)

    return worker_func(func, **kwds)

def validate_worker(func):
    '''Decorator for creating the validate method from simple functions'''

    @functools.wraps(func)
    def validate(self, obj, lazy=True, path=[]):
        try:
            test_ok = func(self, obj)
        except errors.ValidationError as ex:
            ex.path = path
            raise ex
        except Exception as ex:
            msg = 'unhandled exception caught in validation function, %s: %s'
            msg = msg % (type(ex).__name__, ex.message)
            raise RuntimeError(msg)

        if not test_ok:
            msg = 'on key %%(path)s: %s object not a %s' % (type(obj), self)
            raise errors.ValidationError((msg, path))

    return validate


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
