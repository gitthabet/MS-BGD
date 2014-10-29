'''
This module has functions designed to JSON-fy arbitrary Python objects (i.e. 
convert them to JSON structures). 

Users can register converters that convert Python types manually to JSON 
structures. The most simple kind of converter is a Python function that takes an
object of a given type and return a JSON version of it:

>>> def set_convert(obj):
...     """JSON representation of a set."""
...     return {'items': list(obj)} 

This function can be registered using the func:`register` function:

>>> register(frozenset, set_convert)
>>> jsonfy(frozenset([1, frozenset([1, 2])]))
{'items': [1, {'items': [1, 2], u'@type': u'frozenset'}], u'@type': u'frozenset'}

Other types of converters can give the user more control on how the conversion 
is performed. The func:`jsonfy` function also attempts to do an automatic
conversion which works for most pure-Python data types.
'''
from pyson.type_name_utils import type2name, load_modules
from pyson.types import is_object_t
import functools

#===============================================================================
# Register function and converter functions for common datatypes
#===============================================================================
CONVERTERS = {}
def register(tt, function=None, overwrite=False):
    '''Register a converter function for the given type.
    
    Parameters
    ----------
    tt : type
        Class of type to be registered.
    function : callable
        Function that performs the conversion. See func:`jsonfy` for the allowed
        function signatures.
    overwrite : bool
        Forces overwrite of a previous converter for the type ``tt`` if it 
        exists. 
    '''
    # Decorator version of register call
    if function is None:
        return functools.partial(register, tt)

    if not isinstance(tt, type):
        raise TypeError("'tt' must be a type, got %s" % type(tt))
    if tt in CONVERTERS and not overwrite:
        raise ValueError("type %s is already registered" % tt)

    CONVERTERS[tt] = function

do_nothing = lambda x: x
for tt in [int, list, unicode, dict]:
    register(tt, do_nothing)
register(str, unicode)

def jsonfy(obj, json_level=None, print_type=True, invertible=False, recursive=True):
    '''Return a JSON representation of object.
    
    Parameters
    ----------
    obj : anything
        Object to be converted to JSON
    json_level : int
        Maximum JSON level allowed for the given type.
    print_type : bool
        Set to False to prevent adding the ('@type': value) pair to the 
        resulting object. This key is used to convert the JSON object to 
        the appropriate Python type.
    invertible : bool
        If True, the output can be converted back to an identical Python object.
        The default behavior is to allow approximate types, e.g., ``str``
        can be converted to ``unicode``, ``tuple`` to ``list`` and so on.
    recursive : bool
        If False and json_level is respected or not set, it prevents recursive
        application of func:`jsonfy` to child nodes of the JSON result.  
    '''

    tt = type(obj)
    if json_level is not None or invertible:
        raise NotImplementedError

    # Compute the result from the converter function
    try:
        function = CONVERTERS[tt]
    except KeyError:
        function = auto_converter(tt)
    try:
        result = function(obj)
    except Exception as ex:
        msg = 'unhandled exception raised when jsonfy-ing %s object\n    %s: %s'
        msg = msg % (type(obj), type(ex).__name__, ex)
        raise RuntimeError(msg)

    # Print type
    if print_type and not is_object_t(tt):
        try:
            result[u'@type'] = type2name(tt)
        except:
            pass

    #TODO: move recursive to converter function
    if recursive:
        if isinstance(result, dict):
            for k, v in result.items():
                result[k] = jsonfy(v, json_level=json_level, print_type=print_type,
                                      invertible=invertible, recursive=recursive)
        elif isinstance(result, list):
            for idx, v in enumerate(result):
                result[idx] = jsonfy(v, json_level=json_level, print_type=print_type,
                                        invertible=invertible, recursive=recursive)

    return result

def auto_converter(tt):
    '''Auto convert attempt a number of ways of finding appropriate converters 
    to a unhandled type.
    
    The first strategy is to check if the type is supported in the 
    mod:`pyson.jsonfy_extras` module.
    
    If that is not the case, it searches for converters for the superclasses
    of `tt`.
    
    Finally, if that fails an error is raised.
    '''

    # Tries to import a converter from jsonfy_ext.* modules
    name = type2name(tt)
    try:
        load_modules('pyson.jsonfy_extras.ext_' + name)
    except AttributeError:
        pass
    try:
        return CONVERTERS[tt]
    except KeyError:
        pass

    # Tries to use a converter for a base class (hint: this often fails!)
    for base_t in tt.mro()[:-1]:
        try:
            return CONVERTERS[base_t]
        except KeyError:
            pass
    else:
        raise TypeError('object of type %s is not supported' % tt)
        def not_supported(obj):
            raise TypeError('object of type %s is not supported' % tt)
        return not_supported

def attr_fields(attrs, allow_missing=False):
    '''Factory function for converters that take attributes from an object and
    return a dictionary with (attr_name, attr_value) pairs.'''

    attrs = tuple(attrs)

    if allow_missing:
        def converter(obj):
            result = {}
            for attr in attrs:
                try:
                    result[attr] = getattr(obj, attr)
                except AttributeError:
                    pass
            return result
    else:
        def converter(obj):
            values = map(functools.partial(getattr, obj), attrs)
            return dict(zip(attrs, values))

    return converter

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

