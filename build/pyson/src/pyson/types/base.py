'''
Type constants and binary masks
-------------------------------

:mod:`pyson` recognizes a few

'''

from decimal import Decimal
from collections import Mapping, Sequence

#===============================================================================
# Global dicts and constants
#===============================================================================
JSON_TYPE_BITMASKS = {}

JSON_LEVEL_MASK = 0b111

# Type descriptions
OBJECT_T, ARRAY_T, STRING_T, INTEGER_T, REAL_T, BOOLEAN_T, NULL_T, \
    GENERIC_T = [ x << 3 for x in range(8) ]
JSON_TYPE_MASK = 0b111000
JSON_TYPE_DESCR = {
    OBJECT_T: 'OBJECT',
    ARRAY_T: 'ARRAY',
    STRING_T: 'STRING',
    INTEGER_T: 'INTEGER',
    REAL_T: 'REAL',
    BOOLEAN_T: 'BOOLEAN',
    NULL_T: 'NULL',
    GENERIC_T: 'GENERIC',
}

# Type queries
IS_CONTAINER = 1 << 6
IS_NOT_CONTAINER = 0

IS_NUMBER = 1 << 7
IS_NOT_NUMBER = 0

#===============================================================================
# Bitmask manipulation
#===============================================================================
def make_bitmask(json_level, t_code=None):
    '''
    Return the integer value that represents a given JSON type bitmask.
    
    Parameters
    ----------
    json_level : int (0-5)
        Type's JSON json_level.
    t_code : integer ..._T constant
        Numerical code that describes the JSON type of object considered.
        
    Examples
    --------
    >>> x = make_bitmask(1, STRING_T); bin(x)
    '0b10001'
    '''

    if not 0 <= json_level <= 5:
        raise ValueError('json_level must be between 0 and 5')
    elif json_level == 5:
        if t_code is not None:
            raise ValueError('cannot specify type_code for json_level 5 types')
        return 5 | GENERIC_T
    else:
        if t_code is None:
            t_code = GENERIC_T
        is_container = (t_code == OBJECT_T) or (t_code == ARRAY_T)
        is_number = (t_code == INTEGER_T) or (t_code == REAL_T)

        return json_level | t_code | (is_container << 6) | (is_number << 7)


def descr_bitmask(bm):
    '''
    Returns a tuple with (JSON level, type code, is_container, is_value, is_number)
    from a given bitmask.
    
    Examples
    --------
    >>> bm = get_bitmask(str); descr_bitmask(bm)
    (1, 'STRING', False, False)
    '''

    is_container = bool(IS_CONTAINER & bm)
    is_number = bool(IS_NUMBER & bm)
    level = JSON_LEVEL_MASK & bm
    type_code = JSON_TYPE_DESCR[JSON_TYPE_MASK & bm]

    return (level, type_code, is_container, is_number)

def get_bitmask(tt):
    '''
    Return the JSON type description bitmask for the given type ``tt``.
    
    Examples
    --------
    >>> x = get_bitmask(str); bin(x)
    '0b10001'
    '''

    try:
        return JSON_TYPE_BITMASKS[tt]
    except KeyError:
        # Query if any base type is recognized
        bases = tt.mro()[1:]
        if bases[-1] is object:
            bases = bases[:-1]

        # Subtype testing:
        # - Level 0 and 1 subtypes are Level 1 types
        # - Subtypes of non-JSON types are also non-JSON types
        for base in bases:
            try:
                bitmask = JSON_TYPE_BITMASKS[base]
            except KeyError:
                continue

            json_level = bitmask & JSON_LEVEL_MASK
            type_code = bitmask & JSON_TYPE_MASK

            if json_level <= 1:
                return JSON_TYPE_BITMASKS.setdefault(tt, make_bitmask(1, type_code))
            if json_level == 5:
                return JSON_TYPE_BITMASKS.setdefault(tt, make_bitmask(5))

        # Test abstract classes for level 1 object and array types
        if issubclass(tt, Mapping):
            return JSON_TYPE_BITMASKS.setdefault(tt, make_bitmask(1, OBJECT_T))
        if issubclass(tt, Sequence):
            return JSON_TYPE_BITMASKS.setdefault(tt, make_bitmask(1, ARRAY_T))

        # Is a non-json type
        #FIXME: is this the right behavior?
        # this was done originally to accept datetime objects
        return make_bitmask(5)

#===============================================================================
# Fill in default bitmasks
#===============================================================================
JSON_TYPE_BITMASKS.update({
    # Level 0
    dict: make_bitmask(0, OBJECT_T),
    list: make_bitmask(0, ARRAY_T),
    unicode: make_bitmask(0, STRING_T),
    int: make_bitmask(0, INTEGER_T),
    Decimal: make_bitmask(0, REAL_T),
    bool: make_bitmask(0, BOOLEAN_T),
    type(None): make_bitmask(0, NULL_T),

    # Level 1
    Mapping: make_bitmask(1, OBJECT_T),
    Sequence: make_bitmask(1, ARRAY_T),
    basestring: make_bitmask(1, STRING_T),
    float: make_bitmask(1, REAL_T),

    # Non JSON
    type(lambda: None): make_bitmask(5, None),
    type: make_bitmask(5, None),
})

#===============================================================================
# Query functions
#===============================================================================
def has_json_level_t(tt, json_level=4):
    '''Return True if ``tt`` is of a JSON level smaller than ``json_level``. 
    
    If ``json_level`` is not given, tests if it is a valid JSON (i.e. JSON level 
    lesser than 5).'''

    bm = get_bitmask(tt)
    return (JSON_LEVEL_MASK & bm) <= json_level

def has_json_level(obj, json_level=4):
    '''Return True if ``obj`` is of a JSON level smaller than ``json_level``. 
    
    If ``json_level`` is not given, tests if it is a valid JSON (i.e. JSON level 
    lesser than 5).'''

    return has_json_level_t(type(obj), json_level)

def is_container_t(tt, json_level=None):
    'Return True if ``tt`` is a valid container type.'

    bm = get_bitmask(tt)
    if json_level is None:
        return bool(IS_CONTAINER & bm)
    else:
        return bool(IS_CONTAINER & bm and ((JSON_LEVEL_MASK & bm) <= json_level))

def is_container(obj, json_level=None):
    'Return True if ``obj`` is a valid container.'

    return is_container_t(type(obj), json_level)

def is_value_t(tt, json_level=None):
    'Return True if ``tt`` is a valid atomic type.'

    bm = get_bitmask(tt)
    if json_level is None:
        return not bool(IS_CONTAINER & bm)
    else:
        return bool(not (IS_CONTAINER & bm) and ((JSON_LEVEL_MASK & bm) <= json_level))

def is_value(obj, json_level=None):
    'Return True if ``obj`` is a valid atomic object.'

    return is_value_t(type(obj), json_level)

def is_number_t(tt, json_level=None):
    'Return True if ``tt`` is a valid number type.'

    bm = get_bitmask(tt)
    if json_level is None:
        return bool(IS_NUMBER & bm)
    else:
        return bool(IS_NUMBER & bm and ((JSON_LEVEL_MASK & bm) <= json_level))

def is_number(obj, json_level=None):
    'Return True if ``obj`` is a valid number.'

    return is_number_t(type(obj), json_level)
#===============================================================================
# Programaticaly created query functions
#===============================================================================
def query_factory(tname, tcode):
    '''The other query functions are so similar among themselves that is possible to 
    create them programaticaly by this factory function'''
    def query_func_t(tt, json_level=None):
        bm = get_bitmask(tt)
        is_type = (bm & JSON_TYPE_MASK) == tcode
        if json_level is None:
            return is_type
        else:
            return bool(is_type and ((JSON_LEVEL_MASK & bm) <= json_level))

    query_func_t.func_name = 'is_%s_t' % tname
    query_func_t.func_doc = 'Return True if ``tt`` is a valid %s type.' % tname

    def query_func(obj, json_level=None):
        bm = get_bitmask(type(obj))
        is_type = (bm & JSON_TYPE_MASK) == tcode
        if json_level is None:
            return is_type
        else:
            return bool(is_type and ((JSON_LEVEL_MASK & bm) <= json_level))

    query_func.func_name = 'is_%s' % tname
    query_func.func_doc = 'Return True if ``obj`` is a valid %s.' % tname

    return query_func_t, query_func

is_object_t, is_object = query_factory('object', OBJECT_T)
is_array_t, is_array = query_factory('array', ARRAY_T)
is_string_t, is_string = query_factory('string', STRING_T)
is_integer_t, is_integer = query_factory('integer', INTEGER_T)
is_real_t, is_real = query_factory('real', REAL_T)
is_boolean_t, is_boolean = query_factory('boolean', BOOLEAN_T)
is_null_t, is_null = query_factory('null', NULL_T)
is_generic_t, is_generic = query_factory('generic', GENERIC_T)

namespace = globals()
for (tcode, tname) in JSON_TYPE_DESCR.items():
    tname = tname.lower()
    tfunc_t, tfunc = query_factory(tname, tcode)
    namespace[tfunc_t.func_name] = tfunc_t
    namespace[tfunc.func_name] = tfunc

#===============================================================================
# __all__ list with functions and constants to be imported 
#===============================================================================
#__all__ = [ 'has_json_level']
#names = dir()
#
## add query funcs of the form is_...()
#__all__.extend(x for x in dir() if x.startswith('is_'))
#
## add bitmask manipulation functions of the form ..._bitmap()
#__all__.extend(x for x in dir() if 'bitmask' in x)
#
## add uper caps constants
#__all__.extend(x for x in dir() if x.isupper())
#
#print __all__
__all__ = ['has_json_level', 'is_array', 'is_array_t', 'is_boolean',
           'is_boolean_t', 'is_container', 'is_container_t', 'is_generic',
           'is_generic_t', 'is_integer', 'is_integer_t', 'is_null',
           'is_null_t', 'is_number', 'is_number_t', 'is_object', 'is_object_t',
           'is_real', 'is_real_t', 'is_string', 'is_string_t', 'is_value',
           'is_value_t', 'descr_bitmask', 'get_bitmask', 'make_bitmask',
           'ARRAY_T', 'BOOLEAN_T', 'GENERIC_T', 'INTEGER_T', 'IS_CONTAINER',
           'IS_NOT_CONTAINER', 'IS_NOT_NUMBER', 'IS_NUMBER', 'JSON_LEVEL_MASK',
           'JSON_TYPE_BITMASKS', 'JSON_TYPE_DESCR', 'JSON_TYPE_MASK', 'NULL_T',
           'OBJECT_T', 'REAL_T', 'STRING_T']

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
