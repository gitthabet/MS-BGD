from __future__ import absolute_import
from propertylib import auto_property, default_property
from pyson.schema import errors
from pyson.schema.util import get_schemas, from_simple
from pyson.types import is_object_t, is_array_t
import pyson.serialize

# Hold an arbitrary reference to an object to tell that its value is undefined
class Undefined(object):
    def __str__(self):
        return '<undefined>'
undefined = Undefined()

#===============================================================================
#                             Base Schema class
#===============================================================================
class Schema(object):
    # Constants ----------------------------------------------------------------
    # Controls the default behavior for enabling/disabling complete error 
    # messages
    _DEBUG = __debug__

    # Internal counter to track the order of creation of each instance
    _INSTANCE_COUNTER = 0

    # Default null value. Can be overiden in child classes
    NULL = None

    # Special attributes and root information ----------------------------------
    INFO_ATTRIBUTES = ['default', 'parent', 'null', 'name', 'desc', 'label',
                       'label_plural', 'is_optional', 'is_ref', 'is_unique',
                       'is_root', '_ordering_index']
    EXTRA_ATTRIBUTES = [ 'root', 'default_or_null' ]

    class META(object):
        def update_attrs(self, dic):
            for k, v in dic.items():
                setattr(self, k, v)

    # Schemas ------------------------------------------------------------------
    # This validation classes will be fed here once the classes are defined.
    # It is used internally in order to instancialize useful Schema objects
    # when Schema() is invoked    
    OBJECT_SCHEMA = None
    ARRAY_SCHEMA = None
    CTE_SCHEMA = None
    AND_SCHEMA = None
    OR_SCHEMA = None

    #===========================================================================
    # Initialization
    #===========================================================================
    def __new__(cls, *args, **kwds):
        # If Schema() is called directly, it will choose an appropriate 
        # constructor and initialize a subclass.
        if cls is Schema:
            if not args:
                raise TypeError('Schema() takes at least one positional argument (0 given)')
            tt = type(args[0])

            # Choose the correct constructor from the type of the 1st argument
            if is_object_t(tt):
                return cls.OBJECT_SCHEMA(*args, **kwds)
            elif is_array_t(tt):
                return cls.ARRAY_SCHEMA(*args, **kwds)
            else:
                return cls.CTE_SCHEMA(*args, **kwds)

        # This is path is called when Schema.__new__() is called from a subclass 
        else:
            return object.__new__(cls)

    def __init__(self, default=undefined, **kwds):
        """
        Base class for validation of JSON-like objects. 
        
        Parameters
        ----------
        
        default : JSON-like
            Default value of the field. Subclasses should generally use the 
            default value as the first positional argument. The default value
            must validate.
        null : JSON-like
            The null value for the field. It is ``None`` for most fields, but it
            might make sense to assign a different value.
        label : str
            Optional label. Used to print error messages.
        desc : str
            Object's description. Useful if one wants to introspect the schema.
            
        Observations
        ------------
                
        The distinction between the ``null`` and ``default`` fields can be 
        subtle. When the field is absent in a JSON structure, the Schema objects
        can fill in the missing values by first querying ``default``, and if it
        does not exist, it queries ``null``.
          
        The ability to change the null value of the field is specially useful 
        in Str fields. The default behavior distinguishes "the field is empty" 
        (in which the field evaluates to None) from "the field is filled with 
        an empty string". If this distinction is not desirable, one should 
        assign default='', making empty Str fields evaluate to '' rather than 
        None.
        
        An important  difference is that the ``null`` value does not need to 
        validate, while the ``default`` value must.
        
        Examples
        --------
        
        A validator that tests if numbers are greater than 3.1415

        >>> from pyson.schema import *
        >>> class GreaterThanPi(Number):
        ...     @from_simple
        ...     def validate(self, obj):
        ...         super(GreaterThanPi, self).validate(obj)
        ...         return obj > 3.1415
        >>> GreaterThanPi().is_valid(1)
        False
        >>> GreaterThanPi().is_valid(5)
        True
        >>> GreaterThanPi().is_valid('some string')
        False
        """

        # In order to keep a consistent order across fields, this class keeps
        # a global counter thar is incremented every time a new instance of a 
        # Schema sublcass is instantiated.
        Schema._INSTANCE_COUNTER += 1
        self._ordering_index = Schema._INSTANCE_COUNTER

        # Save and validate the default value
        if default is not undefined:
            self.default = default
            self.validate(self.default)

        # Get other parameters from dictionary
        try:
            kwds['is_unique'] = bool(kwds['is_ref'])
        except KeyError:
            pass
        for k in kwds.keys():
            if k in self.INFO_ATTRIBUTES:
                setattr(self, k, kwds.pop(k))

        # Fill-in the root attributes
        self.root = self.META()
        self.root.update_attrs(kwds)

    #===========================================================================
    # Class methods for debugging control
    #===========================================================================
    #TODO: we seem to not be using these methods anymore...
    @classmethod
    def debug_on(cls):
        '''Enable full error messages.'''
        if cls is Schema:
            Schema._DEBUG = True
        else:
            raise TypeError('Debug status can only be set from the Schema class, but not subclasses.')

    @classmethod
    def debug_off(cls):
        '''Disable full error messages.'''
        if cls is Schema:
            Schema._DEBUG = False
        else:
            raise TypeError('Debug status can only be set from the Schema class, but not subclasses.')

    @classmethod
    def query_debug(cls, force=None):
        '''Returns the debug status if ``force`` is None or return ``force`` 
        otherwise. 
        
        This function useful for deciding the default debug status in a user 
        created subclass.
        '''

        if force is None:
            return cls._DEBUG
        else:
            return force

    #===========================================================================
    # Validation
    #===========================================================================
    def validate(self, obj, lazy=True, path=[]):
        """Raise a ValidationError exception if 'obj' does not conform to 
        the given JSON-schema.
        
        Parameters
        ----------
        
        obj : JSON-like
            Object to be validated.
        lazy : bool
            If True (default), it will validate objects with a missing 
            obligatory field if the field has a ``default`` value.
        path : list
            Path for the object in the main JSON structure. 
            
        Examples
        --------
        
        >>> from pyson.schema import *
        >>> schema = Schema({'name': Str(), 'age?': Int(), 'color': Str('blue') })
        
        Valid object: nothing happens
        
        >>> schema.validate({'name': 'Arthur'})
        
        Defaults are filled implicitly, but this can be overridden
        
        >>> schema.validate({'name': 'Arthur'}, lazy=False)
        Traceback (most recent call last):
         ...
        MissingKeyError: missing key: $.color
        
        Invalid object: the field 'favorite_color' is not present in the
        Schema. 
        
        >>> schema.validate({'name': 'Arthur', 'favorite_color': 'Blue'})
        Traceback (most recent call last):
         ...
        InvalidKeyError: invalid key: $.favorite_color
        
        Notes
        -----
        
        This function can be overridden in child classes, but it is often more
        convenient use the func:`pyson.schema.util.from_simple` decorator to 
        provide only a minimal implementation for this function.
        """

        raise NotImplementedError

    def is_valid(self, obj, lazy=True):
        """Return True if 'obj' is valid and False otherwise. 
        
        Notes
        -----
        
        Subclasses should not override this function. See `Schema.validate` 
        instead."""

        try:
            self.validate(obj, lazy)
            return True
        except errors.ValidationError:
            return False

    #===========================================================================
    # Transformations
    #===========================================================================
    @staticmethod
    def as_schema(obj):
        '''
        Return obj if it is a schema and tries to construct a valid schema out
        of obj otherwise.  
        '''

        if isinstance(obj, Schema):
            return obj
        elif isinstance(obj, type) and issubclass(obj, Schema):
            return obj()
        else:
            return Schema(obj)

    def copy(self, keep_parent=True):
        '''Deep copy of schema object. This method is useful in order to define
        fields with identical behavior.
        
        Parameters
        ----------
        
        keep_parent : bool
            If True (default), it keeps the same parent for the copy. Otherwise,
            the copy is created without a parent.
            
        Notes
        -----
        
        A similar, but more flexible, behavior can be obtained calling the 
        Schema object. See `Schema.__call__` for info.'''

        # Copy object by updating its dict
        new = object.__new__(type(self))
        for k, v in self.__dict__.items():
            setattr(new, k, v)
        new.root = self.META(**self.root.__dict__)

        # Update counter
        Schema._INSTANCE_COUNTER += 1
        new._ordering_index = Schema._INSTANCE_COUNTER

        # Save parent
        if not keep_parent:
            new.parent = None
        return new

    def _expand_or_compress(self, is_expand, obj, **kwds):
        '''Many objects have the same or similar behaviors under expansion and 
        compression. The two functions can be implemented together by subclasses
        simply overriding this method.
        
        The first argument ``is_expand`` tells if the operation is an expansion
        or a compression and the other arguments are the same of the 
        corresponding `Schema.expand` and `Schema.compress` methods.'''

        # Only container objects must do something when expanding.
        # Most objects simply return themselves.
        if  obj == self.null:
            return self.null

        if kwds.get('validate', False):
            self.validate(obj, **kwds)

        return obj

    def expand(self, obj, use_default=True, inplace=False, **kwds):
        """Return a copy of ``obj`` with all optional empty fields assigned to 
        their ``default`` or ``null`` values. 
        
        Parameters
        ----------
        
        obj : JSON-like
            Object to do expansion.
        use_default : bool
            If False, it will not expand default values.   
        inplace : bool
            If True, it will perform the expansion inplace instead of creating 
            a copy. Immutable types are insensitive to this argument.
        
        Notes
        -----
        
        In most fields, ``null`` is mapped to Python's None. However, container
        fields such as Object and Array use respectively {} and [] as the 
        default 'null' value. This can be overridden by the keyword argument 
        'null' on object's initialization. 
        
        Users may find more convenient to override `Schema._expand_or_compress` 
        method in subclasses.
        
        Examples
        --------
        
        Expand the default value
        
        >>> from pyson.schema import *
        >>> schema = Schema({'name': Str(), 'age': Int(18)})
        >>> schema.expand({'name': 'Chips'})
        {u'age': 18, u'name': 'Chips'}
        
        Fill empty entries with null
        
        >>> schema = Schema({'name': Str(), 'age?': Int()})
        >>> schema.expand({'name': 'Chips'})
        {u'age': None, u'name': 'Chips'}
        """

        return self._expand_or_compress(True, obj, **kwds)

    def compress(self, obj, use_default=True, inplace=False, **kwds):
        """Return a copy of ``obj`` omitting all optional fields that are equal
        to their ``default`` or ``null`` values (if ``default`` does not exist).
        
        Parameters
        ----------
        
        obj : JSON-like
            Object to do expansion.
        use_default : bool
            If False, it will not expand default values.   
        inplace : bool
            If True, it will perform the expansion inplace instead of creating 
            a copy. Immutable types are insensitive to this argument.
        
        Notes
        -----
        
        Users may find more convenient to override `Schema._expand_or_compress` 
        method in subclasses.
        
        Examples
        --------
        
        Remove default values
        
        >>> from pyson.schema import *
        >>> schema = Schema({'name': Str(), 'age': Int(18)})
        >>> schema.compress({'name': 'Chips', 'age': 18})
        {u'name': 'Chips'}
        
        Remove null
        
        >>> schema = Schema({'name': Str(), 'age?': Int()})
        >>> schema.compress({'name': 'Chips', 'age': None})
        {u'name': 'Chips'}
        """

        return self._expand_or_compress(False, obj, **kwds)

    def adapt(self, obj, inplace=False, path=[]):
        '''
        Adapts an object to be compatible with the schema. This is useful,
        for instance, to load JSON representations of objects into valid
        versions of these objects.
        
        Other common conversions are also implemented (e.g., ints to floats,
        str to unicode)
        
        Examples
        --------
        
        >>> from pyson.schema import *
        >>> schema = Schema({'name': Str(), 'age': Int()})
        >>> schema.adapt({'name': 'Arthur', 'age': 31.0})
        {'age': 31, 'name': 'Arthur'}
        '''
        if self.is_valid(obj):
            return obj
        else:
            msg = 'in %%(path)s: %s object not compatible with %s' % (type(obj), self)
            raise errors.AdaptationError((msg, path))

    def is_default(self, obj):
        '''Return True if ``obj`` is equal to schema's ``default`` value.'''
        try:
            return self.default == obj
        except AttributeError:
            return False

    def can_be_empty(self, use_default=True):
        '''Return True if object can be empty'''

        if  self.is_optional:
            return True
        else:
            if use_default:
                return hasattr(self, 'default')
            else:
                return False

    def obj_from_string(self, obj, validate=True):
        '''Converts a string representation of ``obj`` into a string. 
        Usually, this is a conversion from a JSON representation. 
        
        However, subclasses may define different serializations.'''

        try:
            obj = pyson.serialize.loads(obj)
        except ValueError as ex:
            msg = "%s: '%s' as %s()" % (ex, obj, type(self).__name__)
            raise ValueError(msg)

        if validate:
            self.validate(obj)
        return obj

    #===========================================================================
    # Magical methods
    #===========================================================================
    def __str__(self):
        if self.name:
            return "<%s '%s'>" % (type(self).__name__, self.name)
        else:
            return "<%s>" % type(self).__name__

    def __unicode__(self):
        return unicode(str(self))

    def __and__(self, other):
        '''x.__and__(y) <==> x ^ y'''
        return self.AND_SCHEMA(self, self.as_schema(other))

    def __or__(self, other):
        '''x.__or__(y) <==> x | y'''
        return self.OR_SCHEMA(self, self.as_schema(other))

    def __call__(self, **kwds):
        '''
        Creates a copy of itself and initializes it using (possibly) different 
        parameters. By calling a schema object one can create a copy and 
        simultaneously reset any desired property (default value, desc, label, 
        etc). 
        
        The default value can only be set explicitly as a keyword argument.
        
        Example
        -------
        
        >>> from pyson.schema import *
        >>> v1 = Str(null='', label='Some string')
        >>> v2 = v1(label='Other string')
        >>> v1.null == v2.null
        True
        >>> v2.label
        'Other string'
        '''

        new = self.copy()
        for attr, v in kwds.items():
            if attr in new.INFO_ATTRIBUTES:
                setattr(new, attr, v)
            else:
                setattr(new.root, attr, v)
        return new

    #===========================================================================
    # Object's location within JSON structure 
    #===========================================================================
    def basepath(self):
        '''
        Location of root's object within the JSON structure.
        
        Example
        -------
        
        >>> from pyson.schema import *
        >>> sch = Schema({
        ...     'foobar': {
        ...         'foo': Int(), 
        ...         'bar': Real()
        ...     }
        ... })
        >>> sch['foobar']['bar'].basepath()
        [u'foobar', u'bar']
        '''

        path = []
        node = self
        while node is not None:
            path.append(node.name)
            node = node.parent
        path.pop()
        path.reverse()

        return path

    #===========================================================================
    # Properties
    #===========================================================================
    _NONE = object()
    def get_value(self, key, other=_NONE):
        '''
        Return the value of property ``key`` or ``other`` if the property does
        not exist.
        
        Examples
        --------
        
        >>> from pyson.schema import *
        >>> sch = Str(null='<empty>', ham='spam')
        >>> sch.get_value('null')
        '<empty>'
        >>> sch.get_value('ham')
        'spam'
        
        Raises a KeyError if value does not exist
        
        >>> sch.get_value('foo') #doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: "<class '...Str'> has no property 'foo'"
        
        Or return the optional value if the ``other`` value is defined
        
        >>> sch.get_value('foo', 'bar')
        'bar'
        
        
        '''

        try:
            return getattr(self, key)
        except AttributeError:
            try:
                return getattr(self.root, key)
            except AttributeError:
                if other is self._NONE:
                    raise KeyError("%s has no property '%s'" % (type(self), key))
                else:
                    return other

    #===========================================================================
    # Properties
    #===========================================================================
    parent = default_property(None)

    @auto_property
    def null(self):
        return self.NULL

    @auto_property
    def default_or_null(self):
        try:
            return self.default
        except AttributeError:
            return self.null

    name = default_property(u'')
    desc = default_property(u'')

    @auto_property
    def label(self):
        return self.name.title().replace('_', ' ')

    @auto_property
    def label_plural(self):
        return self.label + 's'

    is_optional = default_property(False)
    is_root = default_property(False)

class Cte(Schema):
    '''
    Examples
    --------
    
    >>> Cte(42).is_valid(42)
    True
    >>> Cte(42).is_valid(12)
    False
    '''

    def __init__(self, cte, **kwds):
        self.cte_value = cte
        super(Cte, self).__init__(cte, **kwds)

    def validate(self, obj, use_default=True, path=[]):
        if obj != self.cte_value:
            msg = "expected '%s', got '%s'" % (self.cte_value, obj)
            raise errors.ValidationError((msg, path))

class Anything(Schema):
    '''
    A validator that validates any object. 
    
    Examples
    --------
    
    >>> Anything().is_valid('Forty two')
    True
    >>> Anything().is_valid(42)
    True
    >>> Anything().is_valid(None)
    True
    '''

    @from_simple
    def validate(self, obj):
        return True

class Nothing(Schema):
    '''
    A validator that invalidates all objects.
    
    Examples
    --------
    
    >>> Nothing().is_valid('Forty two')
    False
    >>> Nothing().is_valid(42)
    False
    >>> Nothing().is_valid(None)
    False
    '''
    @from_simple
    def validate(self, obj):
        return False

# Save specialized schema into the Schema class
Schema.CTE_SCHEMA = Cte

__all__ = get_schemas(globals()) + ['undefined']
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
