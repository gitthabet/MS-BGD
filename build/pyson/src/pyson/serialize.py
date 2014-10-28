r'''
Loading JSON data
=================

The :mod:`pyson` library has simple support to serialization and de-serialization
of JSON objects to/from files and strings. It does not offer an independent
implementation, but rather tries to use the fastest JSON implementation 
available in your system that supports the required operations. The interface 
is uniform and resembles that of the :mod:`json` module present in the standard 
library.    

Encoding basic Python object hierarchies::

    >>> import pyson
    >>> pyson.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    u'["foo", {"bar": ["baz", null, 1.0, 2]}]'
    >>> print pyson.dumps(u'\u1234')
    "\u1234"
    >>> print pyson.dumps('\\')
    "\\"

Decoding JSON::

    >>> import pyson
    >>> pyson.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    [u'foo', {u'bar': [u'baz', None, Decimal('1.0'), 2]}]
    >>> pyson.loads('"\\"foo\\bar"')
    u'"foo\x08ar'

The list of default type translations can be found in :mod:`pyson.types`

API Documentation
-----------------

'''
__all__ = ['dump', 'dumps', 'load', 'loads', 're_encode']

#TODO: full support and investigation over performance claims
# anyjson uses the following list of prefered modules: yajl, jsonlib2, jsonlib
#    simplejson, json, django.utils.simplejson, cjson
#
# Probably cjson is so buggy it should never be loaded. As for 
# django.utils.simplejson, it is behind `json`, which now ships in the standard 
# lib

from decimal import Decimal
try:
    import simplejson as json
except ImportError:
    import json
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from pyson import errors

#===============================================================================
# Serializers
#===============================================================================
def dump(obj, fp):
    '''
    Serialize ``obj`` as a JSON formatted stream to ``fp`` (a ``.write()`` - 
    supporting file - like object).
    '''
    #TODO: implement more complex loaders and test different 3rd party 
    #libraries

    dump_dumb_worker(obj, fp)

def dump_dumb_worker(obj, fp):
    '''
    Serialize obj into fp. No options to control the result
    '''
    json.dump(obj, fp)

def dumps(obj):
    '''
    Similar to ``dump()``, but returns the output as a unicode string.
    '''

    fp = StringIO()
    dump(obj, fp)

    return fp.getvalue().decode('utf8')

#===============================================================================
# De-serializers
#===============================================================================
def load(fp, encoding='utf8'):
    '''
    De-serialize ``fp`` (a ``.read()`` -supporting file-like object containing 
    a JSON document) to a Python object.
    '''

    return loads(fp.read().decode(encoding))


def loads(st, encoding='utf8'):
    '''
    De-serializes a string containing a JSON document to a Python object.
    '''

    if isinstance(st, str):
        st = st.decode(encoding)
    return loads_dumb_worker(st)

def loads_dumb_worker(st):
    try:
        return json.loads(st, parse_float=Decimal)
    except json.JSONDecodeError as ex:
        raise errors.JSONDecodeError(ex.message)

def re_encode(obj, encoder):
    '''Re-encode object using the given type translations'''

    raise NotImplementedError

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
