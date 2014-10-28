import abc
import collections
import fractions
import decimal

#===============================================================================
# Values
#===============================================================================
class Str(object):
    __metaclass__ = abc.ABCMeta
Str.register(basestring)

class Bool(object):
    '''
    Boolean types
    
    >>> isinstance(True, Bool)
    True
    >>> isinstance(False, Bool)
    True
    >>> isinstance(1, Bool)
    False
    '''
    __metaclass__ = abc.ABCMeta
Bool.register(bool)

class Null(object):
    __metaclass__ = abc.ABCMeta
Null.register(type(None))

class Int(object):
    __metaclass__ = abc.ABCMeta
Int.register(int)
Int.register(long)

class Real(object):
    __metaclass__ = abc.ABCMeta
Real.register(float)
Real.register(decimal.Decimal)
Real.register(fractions.Fraction)

class Number(object):
    __metaclass__ = abc.ABCMeta
Number.register(Int)
Number.register(Real)

class Value(object):
    __metaclass__ = abc.ABCMeta
Value.register(Str)
Value.register(Bool)
Value.register(Null)
Value.register(Number)

#===============================================================================
# Container
#===============================================================================
class Mapping(object):
    __metaclass__ = abc.ABCMeta
Mapping.register(dict)
Mapping.register(collections.Mapping)

class Sequence(object):
    '''
    Examples
    --------
    >>> isinstance([], Sequence)
    True
    
    >>> isinstance('fdsfs', Sequence)
    False
    '''
    __metaclass__ = abc.ABCMeta

Sequence.register(list)
Sequence.register(tuple)

class Container(object):
    __metaclass__ = abc.ABCMeta
Container.register(Sequence)
Container.register(Mapping)

#===============================================================================
# JSON
#===============================================================================
class JSON(object):
    __metaclass__ = abc.ABCMeta
JSON.register(Container)
JSON.register(Value)

__all__ = [ 'Str', 'Bool', 'Int', 'Real', 'Number', 'Value', 'Mapping',
            'Sequence', 'Container', 'JSON', 'Null' ]

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
