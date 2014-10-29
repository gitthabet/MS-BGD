#TODO: merge this work with jsonfy (or discard this section completely)
'''
JSON conversion to arbitrary types
==================================

Python has support to many non-JSON types. Most ``pyson`` functions can work 
with non-JSON data types as any other JSON-supported type. One can query, 
search, iterate and manipulate any dictionary structure containing these types
without additional complications.

However, some functions require a translation to proper JSON. This section 
describes the supported ways to do it.

The `to_json` and `from_json` functions
---------------------------------------

Conversion to/from JSON is performed by the `to_json` and `from_json` functions.
The first function takes any object and tries to represent it as a JSON 
structure of a given JSON level. The second function converts a JSON structure
with a "@type" field into the appropriate Python object.

It is up to the user to ensure that `to_json` has a proper "@type" field in 
order to `to_json` and `from_json` functions be invertible. ``pyson`` implements
automatic conversion to/from many common data types: 

>>> from datetime import date
>>> items = to_json(date(2012, 12, 12)).items()
>>> items.sort(); items
[(u'@type', u'datetime.date'), (u'day', 12), (u'month', 12), (u'year', 2012)]

#>>> from_json(dict(items))
#datetime(2012, 12, 12)

Implementing convertors
-----------------------

Any user created class may define an arbitrary JSON conversion by inheriting 
from the class:`JSONConvertible` class and implementing the ``_from_json_`` 
and ``_to_json_`` methods.

Existing types can be registered as in the example bellow which adds support
to conversion of mod:`datetime.date` objects. First, one must implement the 
``from_json`` and ``to_json`` in a class:`JSONConverter` subclass.    

>>> class DateConverter(JSONConverter):
...  pass

'''
from jsonpickle.util import is_object

# Global dictionary that maps types with the corresponding functions that 
# perform a conversion to JSON
# These functions must have the signature func(obj, json_level)
TO_JSON_CONVERTERS = {}

def to_json(obj, json_level=2, type_field=True):
    '''Convert ``obj`` to a valid JSON structure of (at most) the given 
    ``json_level``.
    
    Parameters
    ----------
    
    obj : any object
        Object to be converted to JSON
    json_level : int
        The maximum JSON type level of the output. The default value of ``2``
        was chosen as the most permissive level which can be reasonably 
        serialized to JSON. 
    type_field : bool
        If False, omits the "@type" field if it exists in the resulting 
        structure.
    
    Examples
    --------

    Conversion is affected by the desired json_level of the output
    
    #>>> to_json(2.0), to_json(2.0, json_level=0)
    #2.0, {'@type': 'float', 'value': Decimal('2')}
    '''

    tt = type(obj)
    try:
        converter = TO_JSON_CONVERTERS[tt]
    except KeyError:
        converter = auto_to_json_register_t(tt)

    out = converter(obj, json_level)

    if not type_field and is_object(obj):
        del out[u'@type']

    return out

def auto_to_json_register_t(tt):
    '''
    This function performs several tests in order to attempt a conversion to 
    JSON. It may cache the result of some tests depending on the type of the 
    first argument in order to speed up further conversions from the same type.
    
    The first test is to check if the object has a _from_json_() method and
    call it.
    '''

    try:
        method = tt._to_json_
    except AttributeError:
        # If type does not have an explicit _to_json_ converter, we try to rely
        # in some of Python's built-in serialization scheme. 
        print TO_JSON_CONVERTERS
        raise NotImplementedError

    to_json_register(tt, method)
    return method

def to_json_register(tt, func):
    TO_JSON_CONVERTERS[tt] = func

import datetime
def datetime_to_json(dt, level):
    fields = u'year month day hour minute second microsecond'.split()
    out = dict((f, getattr(dt, f)) for f in fields)
    out[u'@type'] = u'datetime.datetime'
    return  out
def date_to_json(dt, level):
    fields = u'year month day'.split()
    out = dict((f, getattr(dt, f)) for f in fields)
    out[u'@type'] = u'datetime.date'
    return  out


to_json_register(datetime.datetime, datetime_to_json)
to_json_register(datetime.date, date_to_json)

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

