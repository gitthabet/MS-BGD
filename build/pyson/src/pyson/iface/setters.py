'''
Setting values
==============

There are many different functions that, similarly to `getitem`, provide the
write functionality to JSON structures using paths directly.   

There are many similar functions that differ in the way they handle non-existing
nodes and in the way they distinguish behavior in mappings and sequences 
structures.

The differences can be illustrated in the following example. Consider the 
structure

>>> obj = {'foo': [0, 1, 2]}

The most simple function that manipultes ``obj`` is `updateitem`. This function
replaces the value of an existing path element and raises an error if the 
given path does not exist.

>>> updateitem(obj, '$.foo.0', 'zero'); obj
{'foo': ['zero', 1, 2]}

>>> updateitem(obj, '$.bar.0', 'zero')
Traceback (most recent call last):
...
IndexKeyError: u'$.bar.0 is empty'

A less restrictive version is the `setitem` function, which emulates python's
default behavior of key insertion in dictionaries and lists. It creates new
keys in dictionaries, but does not try to fill up lists in any circunstance.

>>> obj = {}
>>> setitem(obj, '$.spam.ham.eggs', 'ham or spam?'); obj
{'spam': {'ham': {'eggs': 'ham or spam?'}}}


API Documentation
-----------------

'''
from pyson.iface.getters import haspath, as_path, as_str_path, getitem
from pyson.iface.exceptions import IndexKeyError
from pyson.types import is_object

__all__ = [ 'updateitem', 'setitem', 'writeitem' ]

def updateitem(obj, path, value):
    '''
    Updates ``obj``'s ``path`` node to given ``value``. 
    
    Raises
    ------
    IndexKeyError
        If the node is empty.
    '''
    path = as_path(path)

    if haspath(obj, path):
        obj = getitem(obj, path[:-1])
        obj[path[-1]] = value
    else:
        raise IndexKeyError('%s is empty' % as_str_path(path))

def setitem(obj, path, value, newmap=None):
    '''
    Updates ``obj``'s ``path`` node to given ``value``. Recursively creates 
    and updates new keys for mapping containers. 
    
    Parameters
    ----------
    obj : JSON-like
        JSON-like structure.
    path : str or list path
        Any valid JSON path.
    value : object
        Any value to be assigned to the given path node.
    newmap : callable
        Factory function for creating new mappings. By default it tries to use
        the same type as the innermost dictionary. This function, called
        with no arguments, should return a new dictionary-like object.

    Raises
    ------
    IndexKeyError
        If a node in a sequence container is empty. 
    '''

    path = as_path(path)
    curr_obj = obj

    # Find the first empty node
    idx = 0
    objs = [obj]
    for node in path[:-1]:
        try:
            curr_obj = curr_obj[node]
            objs.append(curr_obj)
            idx += 1
        except KeyError:
            break_node = node
            break_obj = curr_obj
            break
        except IndexError:
            path = as_str_path(path[:idx + 1])
            raise IndexKeyError('empty node %s in sequence.' % path)
    else:
        # There is no empty node: assign value
        try:
            curr_obj[path[-1]] = value
            return
        except IndexError:
            raise IndexKeyError('empty node %s in sequence.' % as_str_path(path))

    # An empty node was found: inspect the missing structures
    empty_path = path[idx:]

    # Asserts that no integer index exists for the new nodes: it only fills
    # new dictionaries 
    empty_tt = map(type, empty_path)
    if int in empty_tt:
        raise IndexKeyError('attempt to create sequence')

    # Obtain the factory function for creating new mappings
    if newmap is None:
        objs.reverse()
        for obj in objs:
            if is_object(obj):
                newmap = type(obj)
                break
        else:
            newmap = dict

    # Fill dictionary values
    curr = empty = newmap()
    for node in empty_path[1:-1]:
        curr[node] = newmap()
        curr = curr[node]
    curr[empty_path[-1]] = value

    # Commit new dictionary to 'obj'
    break_obj[break_node] = empty

def writeitem(obj, path, value, newmap=None, newseq=None, newitem=None):
    '''
    In most cases, it behaves like the __setitem__ iterface:
    
        setitem(obj, key, value) <==> obj[key] = value. 
    
    The two optional arguments 'fill' and 'fill_value' defines how list-like 
    sequences are handled if 'key' is an invalid index. 
    
    If 'fill' is True (default) and key == len(obj), thus indices are [0, 1, 
    ..., len(obj) - 1],  'value' is appended to the end of the list. This 
    behavior creates the new entry that is equivalent to 'obj[key] == value'.
    
    If 'fill' is True and key > len(obj), the function checks if the user 
    had defined the 'fill_value' argument. The list is then filled with this 
    value until the obj[key] is reached, and finally value is appended to the 
    list.
    '''
    #TODO: support completion in array objects
    raise NotImplementedError

    path = as_path(path)
    curr_obj = obj

    # Find the first empty node
    idx = 0
    objs = [obj]
    for node in path[:-1]:
        try:
            curr_obj = curr_obj[node]
            objs.append(curr_obj)
            idx += 1
        except KeyError:
            break_node = node
            break_obj = curr_obj
            break
        except IndexError:
            path = as_str_path(path[:idx + 1])
            raise IndexKeyError('empty node %s in sequence.' % path)
    else:
        # There is no empty node: assign value
        try:
            curr_obj[path[-1]] = value
            return
        except IndexError:
            raise IndexKeyError('empty node %s in sequence.' % as_str_path(path))

    # An empty node was found: inspect the missing structures
    empty_path = path[idx:]

    # Asserts that no integer index exists for the new nodes: it only fills
    # new dictionaries 
    empty_tt = map(type, empty_path)
    if int in empty_tt:
        raise IndexKeyError('attempt to create sequence')

    # Obtain the factory function for creating new mappings
    if newmap is None:
        objs.reverse()
        for obj in objs:
            if is_object(obj):
                newmap = type(obj)
                break
        else:
            newmap = dict

    # Fill dictionary values
    curr = empty = newmap()
    for node in empty_path[1:-1]:
        curr[node] = newmap()
        curr = curr[node]
    curr[empty_path[-1]] = value

    # Commit new dictionary to 'obj'
    break_obj[break_node] = empty

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

