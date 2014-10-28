from pyson.schema.schema_class import Schema, Nothing, Anything
from pyson.schema.util import get_schemas, from_simple

class Self(Schema):
    pass

class Null(Schema):
    '''
    Examples
    --------
    
    >>> Null().is_valid(None)
    True
    >>> Null().is_valid(42)
    False
    '''

    @from_simple
    def validate(self, obj):
        return obj is None

#class Choices(Schema):
#    '''
#    Examples
#    --------
#    
#    Tests if object belongs to some set of possibilities
#    
#    >>> sch = Choices(['foo', 'bar', 'ham', 'spam'])
#    >>> sch.is_valid('eggs')
#    False
#    >>> sch.is_valid('ham')
#    True
#    
#    If numeric_choices is True, assumes that arguments are integers
#    
#    >>> sch.is_valid('ham', numeric_choices=True)
#    False
#    >>> sch.is_valid(1, numeric_choices=True)
#    True
#    >>> sch.is_valid(10, numeric_choices=True)
#    False
#    
#    >>> sch.expand('ham', numeric_choices=True)
#    2
#    >>> sch.expand(2, numeric_choices=False)
#    'ham'
#    '''
#    def __init__(self, choices, *args, **kwds):
#        self.choices = list(choices)
#        self.choices_set = set(self.choices)
#        self.choices_map = dict(enumerate(self.choices))
#        self.choices_inverse_map = dict((v, i) for (i, v) in enumerate(self.choices))
#        self.num_choices = len(self.choices)
#
#        super(Choices, self).__init__(*args, **kwds)
#
#    def _validation_function(self, obj, **kwds):
#        if kwds.get('numeric_choices', False):
#            try:
#                return 0 <= obj < self.num_choices
#            except:
#                return False
#        else:
#            return obj in self.choices_set
#
#    def expand(self, obj, **kwds):
#        if 'numeric_choices' not in  kwds:
#            super(Choices, self).expand(obj, **kwds)
#        else:
#            if kwds['numeric_choices']:
#                try:
#                    return self.choices_inverse_map[obj]
#                except KeyError:
#                    try:
#                        if 0 <= obj < self.num_choices:
#                            return obj
#                        else:
#                            raise self.ValidationIndexError('invalid index, %s' % obj)
#                    except:
#                        raise self.ValidationError('invalid choice, %s' % obj)
#            else:
#                try:
#                    return self.choices_map[obj]
#                except KeyError:
#                    if obj in self.choices_inverse_map:
#                        return obj
#                    else:
#                        if isinstance(obj, int):
#                            raise self.ValidationIndexError('invalid index, %s' % obj)
#                        else:
#                            raise self.ValidationError('invalid choice, %s' % obj)

#class Ref(Schema):
#    '''
#    Examples
#    --------
#    
#    Object must be a valid list of integers
#    
#    >>> from pyson.schema import * 
#    >>> fib_list = Array(Int)
#    
#    Retrieves the the list with the first N fibonacci numbers.
#    In the context of this exercise, it is getting a valid fib_list object 
#    from an integer reference N.
#    
#    >>> def get_obj(N):
#    ...     def fib_numbers():
#    ...         a, b = -1, 1
#    ...         for i in range(N):
#    ...             a, b = b, a + b
#    ...             yield b
#    ...     return list(fib_numbers())
#    
#    >>> def get_ref(lst):
#    ...     if lst == get_obj(len(lst)):
#    ...         return len(lst)
#    ...     else:
#    ...         raise ValidationError
#    
#    >>> sch = Ref(fib_list, Int(), get_obj=get_obj, get_ref=get_ref)
#    
#    By default, it checks the object's value
#    
#    >>> sch.is_valid([0, 1, 1, 2])
#    True
#    >>> sch.is_valid(4)
#    False
#    
#    If ``use_ref`` is ``True``, it assumes that object is a reference
#    
#    >>> sch.is_valid(4, use_ref=True)
#    True
#    >>> sch.is_valid([0, 1, 1, 2], use_ref=True)
#    False
#    
#    Reference validators can be expanded into references
#    
#    >>> sch.expand(10, use_ref=False)
#    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
#    
#    >>> sch.expand([0, 1, 1, 2, 3, 5, 8, 13, 21, 34], use_ref=True)
#    10
#    '''
#
#    INFO_ATTRIBUTES = Schema.INFO_ATTRIBUTES + [ 'type', 'ref_type' ]
#
#    def __init__(self, obj_type, ref_type=Nothing(), *args, **kwds):
#        if isinstance(obj_type, basestring):
#            ref_type = Anything()
#        self.type = obj_type
#        self.ref_type = ref_type
#        self.obj_getter = kwds.get('get_obj', None)
#        self.ref_getter = kwds.get('get_ref', None)
#
#        super(Ref, self).__init__(*args, **kwds)
#
#    def _validation_function(self, obj, **kwds):
#        if kwds.pop('use_ref', False):
#            return self.ref_type.is_valid(obj)
#        else:
#            try:
#                return self.type.is_valid(obj, **kwds)
#            except AttributeError:
#                return True
#
#    def expand(self, obj, **kwds):
#        if 'use_ref' in kwds:
#            if kwds['use_ref']:
#                if self.ref_type.is_valid(obj):
#                    return obj
#                else:
#                    return self.get_ref(obj)
#            else:
#                if self.type.is_valid(obj):
#                    return obj
#                else:
#                    return self.get_obj(obj)
#        else:
#            return super(Ref, self).expand(obj, **kwds)
#
#    def get_obj(self, obj):
#        if self.obj_getter is not None:
#            try:
#                return self.obj_getter(obj)
#            except Exception as ex:
#                raise self.ValidationError('invalid reference: %s', ex)
#        else:
#            raise ValueError("must define an 'obj_getter' function")
#
#    def get_ref(self, obj):
#        if self.obj_getter is not None:
#            try:
#                return self.ref_getter(obj)
#            except Exception as ex:
#                raise self.ValidationError('invalid object: %s', ex)
#        else:
#            raise ValueError("must define a 'ref_getter' function")


__all__ = get_schemas(globals())
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
