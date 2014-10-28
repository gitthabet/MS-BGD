from pyson.iface.iterators import _ITERITEMS_FUNCS, _ITERITEMS_ANYITER
__all__ = ['walkitems', 'walkvalues', 'walkpaths']

#TODO: implement recursive walks

def walkitems(obj, anyiter=False, max_nest=None):
    '''
    Iterate over all pairs of (key, obj[key]) in obj. 
    
    If 'obj' is a mapping, iteritems(obj) is equivalent obj.iteritems(). If it 
    is a sequence, iteritems(obj) behaves similarly to enumerate(obj).
    
    Arguments
    ---------
    
    obj : any container object (mapping or sequence)
        Object to be iterated
    anyiter : bool
        If 'obj' is iterable but does not support indexing (e.g., an iterator 
        or a set object), the default behavior is to raise a TypeError. If 
        'anyiter' is True, this function works similarly to the enumerate(obj) 
        for these objects.
    
    Examples
    --------
    
    Supports lists and dicts
    
    >>> list(iteritems([1,2])); list(iteritems({'foo': 'bar'})) 
    [(0, 1), (1, 2)]
    [('foo', 'bar')]
    
    Sequence types such as strings are also supported.

    >>> list(iteritems('foo'))
    [(0, 'f'), (1, 'o'), (2, 'o')]
    
    The default behavior is to raise an error if 'obj' does not support 
    indexing.
    
    >>> iteritems(set())
    Traceback (most recent call last):
    ...
    TypeError: object of type <type 'set'> is not supported
    
    If 'obj' is iterable, this behavior can be overridden by setting anyiter to
    True. In this case, the object is treated as a sequence.
    
    >>> list(iteritems(set([1, 2]), anyiter=True))
    [(0, 1), (1, 2)]
    
    See also
    --------
        
    walkpaths()  --- iterate over all paths of 'obj'
    walkvalues() --- iterate over all values of 'obj'
    '''

    #
    # The dict _ITERITEMS_FUNCS caches iterator factory functions for each type
    # There are three types of expansion:
    # 
    #     1) iteritems(obj) <==> obj.iteritems()
    #     2) iteritems(obj) <==> obj.items() # Python 3
    #     3) iteritems(obj) <==> enumerate(obj)
    #     4) iteritems(obj) ---- raises TypeError (obj do not support 
    #                                              __getitem__ and iteration)
    #
    # ITERITEM_TYPES returns a function that creates the corresponding iterator,
    # or None if object is not supported.
    try:
        tt = type(obj)
        iterfunc = _ITERITEMS_FUNCS[tt]
    except KeyError:
        # Checks if object is in black list of anyiter 
        try:
            iterfunc = _ITERITEMS_ANYITER[tt]
        except KeyError:
            # Discovers to which category the object belongs to
            if hasattr(tt, 'iteritems'):
                iterfunc = _ITERITEMS_FUNCS[tt] = tt.iteritems
            elif hasattr(tt, 'items'):
                iterfunc = _ITERITEMS_FUNCS[tt] = tt.items
            # Sequence protocol
            elif hasattr(tt, '__getitem__') and hasattr(tt, '__len__'):
                iterfunc = _ITERITEMS_FUNCS[tt] = enumerate
            # Generic iterator protocol
            elif hasattr(tt, '__iter__'):
                iterfunc = _ITERITEMS_ANYITER[tt] = enumerate
                if not anyiter:
                    iterfunc = None
            else:
                iterfunc = _ITERITEMS_ANYITER[tt] = None
        finally:
            if iterfunc is None:
                raise TypeError('object of type %s is not supported' % type(obj))
    # Return iterator
    return iterfunc(obj)

# Utility functions / variables used by iteritems() ----------------------------
_ITERITEMS_FUNCS = {}
_ITERITEMS_ANYITER = {}

# Functions based on iteritems() -----------------------------------------------
def walkvalues(obj, anyiter=False, max_nest=None):
    '''
    Iterate over all values of 'obj'.
    
    See also
    --------
    
    walkitems()  --- iterate over (key, obj[key]) pairs
    walkpaths()  --- iterate over all paths of 'obj'
    '''
    for (_, v) in walkitems(obj, anyiter, max_nest):
        yield v

def walkpaths(obj, anyiter=False, max_nest=None):
    '''
    Iterate over all keys/indices of 'obj'
    
    See also
    --------
    
    walkitems()  --- iterate over (key, obj[key]) pairs
    walkvalues() --- iterate over all values of 'obj'
    '''
    for (p, _) in walkitems(obj, anyiter, max_nest):
        yield p

def walk(json, base='$'):
    '''
    Return iterator over all items in JSON structure. The iterator yields pairs
    containing the jpath to the item and the corresponding value.
    
    Example
    -------
    
    >>> json = {'ham': {'spam': 'eggs', 
    ...                  'is_good': {'breakfast': True, 'lunch': False}}, 
    ...          'foo': ['bar', 'foobar']}
    >>> for item in sorted(walk(json)):
    ...    print '{0}: {1}'.format(*item)
    $.foo.0: bar
    $.foo.1: foobar
    $.ham.is_good.breakfast: True
    $.ham.is_good.lunch: False
    $.ham.spam: eggs
    '''

    if json is None or isinstance(json, (basestring, int, float, long, bool)):
        yield (base, json)
    else:
        if isinstance(json, (dict, collections.Mapping)):
            iterable = json.items()
        elif isinstance(json, (list, tuple, collections.Iterable)):
            iterable = enumerate(json)
        else:
            yield (base, json)
            #raise TypeError('invalid type, %s' % (type(json).__name__))
        for k, v in iterable:
            for item in walk(v, '%s.%s' % (base, k)):
                yield item

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

