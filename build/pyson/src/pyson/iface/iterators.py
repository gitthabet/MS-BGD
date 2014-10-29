__all__ = [ 'iteritems', 'itervalues', 'iterkeys', 'listitems', 'listvalues',
            'listkeys']

def iteritems(obj, anyiter=False):
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
    
    listitems()  --- return a list of all key/values of 'obj'
    iterkeys()   --- iterate over all keys/indices of 'obj'
    itervalues() --- iterate over all values of 'obj'.
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
def itervalues(obj, anyiter=False):
    '''
    Iterate over all values of 'obj'.
    
    See also
    --------
    
    listvalues() --- return a list with all values of 'obj'.
    iteritems()  --- iterate over (key, obj[key]) pairs
    iterkeys()   --- iterate over all keys/indices of 'obj'
    '''
    for (_, v) in iteritems(obj, anyiter):
        yield v

def iterkeys(obj, anyiter=False):
    '''
    Iterate over all keys/indices of 'obj'
    
    See also
    --------
    
    listkeys()   --- return a list of all keys/indices of 'obj'
    iteritems()  --- iterate over (key, obj[key]) pairs
    itervalues() --- iterate over all values of 'obj'.
    '''
    for (k, _) in iteritems(obj, anyiter):
        yield k

def listitems(obj, anyiter=False):
    '''Version of iteritems that returns a list instead of an iterator.'''

    return list(iteritems(obj, anyiter))

def listvalues(obj, anyiter=False):
    '''Version of itervalues that returns a list instead of an iterator.'''

    return list(itervalues(obj, anyiter))

def listkeys(obj, anyiter=False):
    '''Version of iterkeys that returns a list instead of an iterator.'''

    return list(iterkeys(obj, anyiter))

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

