from pyson.schema.sch_containers import Array, Object
from pyson.schema.schema_class import Schema, undefined
from pyson.schema.util import get_schemas, from_simple

class Type(Schema):
    '''
    Schema that tests if object is of given type.
    
    Examples
    --------
    
    >>> Type(float).is_valid(42.0)
    True
    >>> Type(float).is_valid(42)
    False
    '''

    def __init__(self, tt, default=undefined, json_equiv=None, **kwds):
        self.type = tt
        self.json_equiv = json_equiv
        super(Type, self).__init__(default, **kwds)

    @from_simple
    def validate(self, obj):
        if self.json_equiv:
            return isinstance(obj, self.type) or self.json_equiv.is_valid(obj)
        else:
            return isinstance(obj, self.type)

def type_schema_factory(tt, name=None):
    '''
    Factory function that creates a new Schema validator that tests if objects
    are of the given type 'tt'.
    
    Examples
    --------
    
    >>> MyFloat = type_schema_factory(float)
    >>> MyFloat().is_valid(1)
    False
    >>> MyFloat().is_valid(1.0)
    True
    '''
    if name is None:
        name = tt.__name__.title()

    @from_simple
    def validate(self, obj):
        return isinstance(obj, tt)

    return type(name, (Schema,), {'validate': validate})

class mk_obj(object):
    class __metaclass__(type):
        '''
        Optional fields should start with double underscores 
        
        Examples
        --------
        
        Schema initialized using the class inheritance notation
        
        >>> from pyson.schema import *
        >>> class Date(mk_obj):
        ...     year = Int()
        ...     month = Int()
        ...     day = Int()
        ...     __is_end_of_the_world = Bool()
        >>> Date().is_valid({'year': 2012, 'month': 12, 'day': 12})
        True
        
        '''
        def __new__(cls, name, bases, dic):
            # Allows the creation of the SchemaObj parent type 
            if name == 'mk_obj':
                return type.__new__(cls, name, bases, dic)

            # No subtypes of SchemaObj will be created, instead they will 
            # instaciate a Object() schema
            del dic['__module__']

            # Find all optional arguments
            mangling = '_%s__' % name
            msize = len(mangling)
            for arg_name in dic.keys():
                if arg_name.startswith(mangling):
                    dic[arg_name[msize:] + '?'] = dic.pop(arg_name)

            try:
                descr = dic['__doc__']
                return Object(dic, name=name, descr=descr)
            except KeyError:
                return Object(dic, name=name)


class mk_array_of(object):
    class __metaclass__(type):
        '''
        Examples
        --------
        
        Schema initialized using the class inheritance notation
        
        >>> from pyson.schema import *
        >>> class DateLst(mk_array_of):
        ...     year = Int()
        ...     month = Int()
        ...     day = Int()
        ...     __is_end_of_the_world = Bool()
        >>> DateLst().is_valid([{'year': 2012, 'month': 12, 'day': 12}])
        True
        
        '''
        def __new__(cls, name, bases, dic):
            # Allows the creation of the SchemaObj parent type 
            if name == 'mk_array_of':
                return type.__new__(cls, name, bases, dic)

            # No subtypes of SchemaObj will be created, instead they will 
            # instaciate a Object() schema
            del dic['__module__']

            # Find all optional arguments
            mangling = '_%s__' % name
            msize = len(mangling)
            for arg_name in dic.keys():
                if arg_name.startswith(mangling):
                    dic[arg_name[msize:] + '?'] = dic.pop(arg_name)

            try:
                descr = dic['__doc__']
                tt = Object(dic, name=name, descr=descr)
            except KeyError:
                tt = Object(dic, name=name)
            return Array(tt)

def is_optional(sch, value=True):
    '''Flag field as optional'''

    sch.is_optional = value
    return sch

def is_root(sch, value=True):
    '''Flag field as root field'''

    sch.is_root = value
    return sch

__all__ = get_schemas(globals()) + ['mk_obj', 'mk_array_of', 'type_schema_factory', 'is_optional', 'is_root']
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
