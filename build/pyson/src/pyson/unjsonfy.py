'''
The functions in this module attempt to do the opposite to the 
mod:`pyson.jsonfy` module and convert JSON structures to Python objects.

In most cases, JSON to object converters can be simple functions. This example
shows how to convert a JSON structure to a ``datetime.date`` object:

>>> from datetime import date
>>> def to_date(json):
...     return date(json['year'], json['month'], json['day'])
>>> register(date, to_date)

The converter is activated using the func:`unjsonfy` function:

>>> unjsonfy({'year': 2012, 'month': 12, 'day': 12}, date)
datetime.date(2012, 12, 12)

The type can be implicit if the JSON object have an apropriate '@type' field:

>>> unjsonfy({'year': 2012, 'month': 12, 'day': 12, '@type': 'datetime.date'})
datetime.date(2012, 12, 12)
'''

from copy import deepcopy
from pyson.type_name_utils import type2name, load_modules
from type_name_utils import name2type

#===============================================================================
# Register function and converter functions for common datatypes
#===============================================================================
CONVERTERS = {}
def register(tt, function, overwrite=False):
    '''Register a converter function for the given type.
    
    Parameters
    ----------
    tt : type
        Class of type to be registered.
    function : callable
        Function that performs the conversion. See func:`unjsonfy` for the 
        allowed function signatures.
    overwrite : bool
        Forces overwrite of a previous converter for the type ``tt`` if it 
        exists. 
    '''
    if not isinstance(tt, type):
        raise TypeError("'tt' must be a type, got %s" % type(tt))
    if tt in CONVERTERS and not overwrite:
        raise ValueError("type %s is already registered" % tt)

    CONVERTERS[tt] = function

def unjsonfy(json, tt=None, recursive=True, inplace=False, lazy=True):
    '''Create object from its JSON representation
    
    Parameters
    ----------
    json : JSON-like
        JSON-like structure to be converted to a Python object.
    tt (optional): type
        Type of the output object (can be inferred from the '@type' key, if 
        ``json`` has it. 
    recursive : bool
        If False, prevents recursive application of func:`jsonfy` to child nodes 
        of the JSON input.
    '''

    if tt is None:
        try:
            tt = json[u'@type']
        except:
            if not lazy:
                raise ValueError("'tt' must be set explicity if 'json' does not have a '@type' key")
            else:
                tt = None
        else:
            tt = name2type(tt)

    #TODO: move 'inplace' and 'recursive' to the converter function 
    if not inplace:
        json = deepcopy(json)
    if recursive:
        if isinstance(json, dict):
            for k, v in json.items():
                json[k] = unjsonfy(v, recursive=True, inplace=True)
        elif isinstance(json, list):
            for idx, v in enumerate(json):
                json[idx] = unjsonfy(v, recursive=True, inplace=True)

    # Compute the result from the converter function
    try:
        converter = CONVERTERS[tt]
    except KeyError:
        # Tries to load converters from unjsonfy_extras
        try: load_modules('pyson.unjsonfy_extras.ext_' + type2name(tt))
        except AttributeError: pass

        try:
            converter = CONVERTERS[tt]
        except KeyError:
            if tt is None:
                return json
            raise ValueError('there is no known converter to type %s' % tt)

    return converter(json)

def callfunc(tt, json_t=dict):
    '''Factory function for converter methods threturn at call a function using 
    object as *args or **kwds depending on the value of json_t variable.'''

    if json_t is dict:
        def converter(obj):
            kwds = obj.copy()
            kwds.pop('@type', None)
            return tt(**kwds)
    elif json_t is list:
        def converter(obj):
            args = obj
            return tt(*args)
    else:
        raise ValueError('json_t must be list or dict')

    return converter

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

