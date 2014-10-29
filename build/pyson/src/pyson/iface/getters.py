r'''
JSON Paths
==========

JSON-like structures can be represented by combinations between dictionaries 
and lists, with simple immutable types in its nodes. Given the JSON-like 
structure

>>> obj = { "store": {\
...     "book": [ 
...       { "category": "reference",
...         "author": "Nigel Rees",
...         "title": "Sayings of the Century",
...         "discount price": 8.95
...       },
...       { "category": "fiction",
...         "author.name": "Evelyn",
...         "title": "Sword of Honour",
...         "price": 12.99
...       }
...     ]
...   }
... }

Each datum can be addressed by its corresponding address. For example, the 
author "Nigel Rees" can be found under "store", and is the "author" key in the
first "book". This address can be represented by a list of the key and indices 
used to access this information in the data structure, i.e.,   
``['store', 'book', 0, 'author']``. Additionally, these paths can be 
represented by strings, using the notation ``'$.store.book.0.author'``, in 
which ``$`` represents the root node. 

The `as_path` and `as_str_path` functions can convert between the string and 
list representations of these addresses

>>> as_path('$.store.book.0.author')
['store', 'book', 0, 'author']

The items can be accessed uniformly using the `getitem` function using the
string or list notations to represent paths.

>>> getitem(obj, '$.store.book.0.author')
'Nigel Rees'

There is no requirement that the items in a path list should be strings or 
integers. In fact, they can be anything and it is up to the container structures
to support them or not. String paths are more restrictive in which only strings
and integers are allowed. This is more conformant with the JSON spec. 

String keys can be enclosed by quotation marks in order to represent more
complicated values, as in
  
>>> getitem(obj, '$.store.book.0."discount price"')
8.95

One can also test if a given node exists

>>> haspath(obj, '$.store.10."number of viewers"')
False

Notes
-----

This standard is vaguely based on the notation defined at
http://goessner.net/articles/JsonPath/.

Doctests
--------

(Probably this should go to a test module...)
Converting complicated list paths to string paths

>>> as_str_path(['foo', 1, 'bar'])
u'$.foo.1.bar'

>>> as_str_path(['my root', 0, 'she said: "yeah!"'])
u'$."my root".0."she said: \\"yeah!\\""'

API Documentation
-----------------
'''
from pyson.iface.exceptions import *
import re

__all__ = [ 'getitem', 'haspath', 'as_path', 'as_str_path' ]

# Matches alphanumeric names or strings similar to those defined in 
# tokenize.String 
RE_PATH_NODE = re.compile(
    r'''^[ ]*(?P<name>[a-zA-Z]\w*)|(?P<int>-?\d+)|(?P<str1>'[^\n'\\]*(?:\\.[^\n'\\]*)*')|(?P<str2>"[^\n"\\]*(?:\\.[^\n"\\]*)*")[ ]*([.]|$)''')

# Matches valid variable names
RE_NAME = re.compile(r'^[a-zA-Z]\w*$')

def as_path(path):
    '''
    Convert a string that represents a JSON path into a tuple.
    '''

    if isinstance(path, (tuple, list)):
        return list(path)

    # Remove dollar sign
    if path.startswith('$.'):
        pattern = path[2:]
    else:
        pre, _, new_path = path.partition('.')
        if not pre.strip() == '$':
            raise ValueError("invalid path '%s', must start with '$.'" % path)
        else:
            pattern = new_path.lstrip()

    # List that accumulates path nodes
    path_nodes = []
    for _i in xrange(1000):
        m = RE_PATH_NODE.match(pattern)
        if m is None:
            if pattern:
                converted = ', '.join(path_nodes)
                msg = "'Invalid path: (%s, ???) from '%s'" % (converted, path)
                raise ValueError(msg)
            else:
                break
        else:
            groups = m.groupdict()

            # Choose action depending on the type of match
            if groups['name'] is not None:
                path_nodes.append(groups['name'])

            elif groups['int'] is not None:
                path_nodes.append(int(groups['int']))

            elif groups['str1'] is not None:
                aux = groups['str1'][1:-1]
                path_nodes.append(aux.replace("\\'", "'"))

            elif groups['str2'] is not None:
                aux = groups['str2'][1:-1]
                path_nodes.append(aux.replace('\\"', '"'))

            else:
                raise RuntimeError

            pattern = pattern[m.end():].lstrip().lstrip('.')
    else:
        raise RuntimeError('Maximum number of nodes reached: 1000')

    return path_nodes

def getitem(obj, path, default=DEFAULT):
    """
    Return the value in a given JSON path of 'obj'. 
    
    Parameters
    ----------
    obj : JSON-like object 
        JSON structure (list-like or dictionary-like)   
    path : str, iterable
        The path can be a string of the form ``"$.child.toys.0"`` or an 
        iterable that expands to ``['child', 'toys', 0]``
    default
        Return this value if `obj` does possess the desired path node. 
    
    Raises
    ------
    KeyIndexError
        If path is not present in `obj'.
        
    """

    curr_idx = 0
    curr_obj = obj
    path = as_path(path)

    try:
        for k in path:
            curr_obj = curr_obj[k]
            curr_idx += 1
        return curr_obj
    except (KeyError, IndexError):
        if default is not DEFAULT:
            return default
        else:
            base = path[:curr_idx]
            if base:
                full_path = as_str_path(base)
            else:
                full_path = 'root node'
            raise IndexKeyError("key does not exist at %s: '%s'" % (full_path, k))

def as_str_path(path):
    '''Represents a given 'path' as a valid query string'''

    if isinstance(path, basestring):
        #TODO: validate string
        return path

    nodes = [u'$']
    for node in path:
        if isinstance(node, basestring):
            node = unicode(node)
            if not RE_NAME.match(node):
                node = node.replace('"', '\\"')
                node = u'"%s"' % node
            nodes.append(node)
        elif isinstance(node, int):
            nodes.append(str(node))
        else:
            raise TypeError("invalid path element of type %s; only int's and str's are accepted" % type(node))

    return u'.'.join(nodes)

def haspath(obj, path):
    '''
    Return True if ``obj`` has a value associated with the given ``path``.  
    '''

    try:
        _aux_value = getitem(obj, path)
        return True
    except IndexKeyError:
        return False

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

