from pyson import types as pyson_t
from pyson.schema.schema_class import Schema, Anything
from pyson.schema.util import get_schemas
from pyson.schema import errors
import collections

class Container(Schema):
    def as_child(self, child):
        '''
        Modify Schema instance to become a child of self.
        '''

        child = self.as_schema(child)
        if not (child.parent is self or child.parent is None):
            name = type(child).__name__
            pname = type(child.parent).__name__
            raise ValueError("'%s' validator already has parent '%s'" % (name, pname))
        child.parent = self
        return child

class Object(Container, collections.Mapping):
    NULL = {}
    INFO_ATTRIBUTES = Container.INFO_ATTRIBUTES + [ '_fields', '_schemas' ]

    def __init__(self, *args, **kwds):
        '''
        Represents a JSON Object. JSON objects are essentially a dictionary
        in which keys must be strings.
        
        Examples
        --------
        
        >>> from pyson.schema import *
        >>> schema = Object({ 'book': Str(), 'answer': Str() | Cte(42) })
        >>> schema.validate({'book': 'HHGTTG', 'answer': 12})
        Traceback (most recent call last):
        ...
        ValidationError: $.answer is none of: 'Cte, Str'
        '''
        # Initialize
        if len(args) == 2:
            schema = args[0]
            args = (args[1],) # default
        elif len(args) == 1:
            schema = args[0]
            args = () # no default
        super(Object, self).__init__(**kwds)

        # Check empty mapping
        if not schema:
            raise ValueError('empty mapping.')

        # Convert _schemas to schema instances (e.g. dicts, become Objects, 
        # strings and ints become constants, etc)
        for k, v in schema.items():
            schema[k] = Schema.as_schema(v)

        # Validation keys correspond to entries in the form of 'string': Schema().
        self._schemas = {}
        self._root_schema = None
        self.root_key = None
        for k, v in schema.items():
            self.add_item(unicode(k), v)

        # Compute the order each field was created
        fields = self._schemas.items()
        if self.root_key is not None:
            fields.append((self.root_key, self._root_schema))
        fields = [ (f._ordering_index, k) for (k, f) in fields ]
        fields.sort(key=lambda x: x[0])
        self._fields = [ k for (_i, k) in fields ]

    def validate(self, obj, lazy=True, path=[]):
        # Check if obj is a dict
        if not pyson_t.is_object(obj):
            msg = "object of type '%s' is not a mapping." % type(obj).__name__
            raise errors.ValidationError((msg, path))

        # Validate root
        obj_keys = set(obj)
        valid_root = False
        if self.root_key is not None:
            try:
                root = obj[self.root_key]
            except KeyError:
                raise errors.MissingKeyError((None, path + [self.root_key]))
            else:
                self._root_schema.validate(root, lazy, path)
                obj_keys.remove(self.root_key)
                valid_root = True

        # Catch errors and re-raise exception as PartialValidation if
        # valid_root is True
        try:
            # Validate all keys
            for key, validator in self._schemas.items():
                # Get value from object and check if key exists
                try:
                    value = obj[key]
                    obj_keys.remove(key)
                except KeyError:
                    if not validator.can_be_empty(lazy):
                        raise errors.MissingKeyError((None, path + [key]))
                else:
                    # Validate value
                    validator.validate(value, lazy, path + [key])

            # Assert obj do not have extra keys
            if obj_keys:
                first_key = iter(obj_keys).next()
                raise errors.InvalidKeyError((None, path + [first_key]))
        except Exception as ex:
            if valid_root:
                raise errors.PartialValidationError(ex)
            else:
                raise ex

    def expand(self, obj, **kwds):
        expanded = {}
        expanded.update((unicode(k), v) for (k, v) in obj.items())
        for key in self:
            if key not in obj:
                try:
                    value = self[key].expand(obj[key], **kwds)
                except KeyError:
                    value = self._schemas[key].default_or_null
                expanded[key] = value
        return expanded

    def compress(self, obj, **kwds):
        '''
        >>> from pyson.schema import *
        >>> schema = Schema({ u'hello': Str(u'world!'), 'ham?': Str(u'spam') })
        >>> schema.compress({ u'hello': u'world!', u'ham': u'eggs' })
        {u'ham': u'eggs'}
        
        >>> schema.compress({ u'hello': u'world!' }, use_default=False)
        {u'hello': u'world!'}
        '''

        compress_defaults = kwds.get('use_default', True)
        compressed = {}
        for k, v in obj.items():
            sch = self[k]
            if v == sch.default_or_null:
                if sch.is_optional or compress_defaults:
                    continue
            compressed[unicode(k)] = sch.compress(v, **kwds)
        return compressed

    def adapt(self, obj, inplace=False, path=[]):
        # Check if obj is a dict
        if not pyson_t.is_object(obj):
            raise errors.AdaptationError(('%(path)s: not a mapping', path))

        new_obj = obj.copy()

        # Test the root key
        root_value = None
        if self.root_key is not None:
            try:
                root_value = new_obj.pop(self.root_key)
            except KeyError:
                raise errors.AdaptationError((None, path))
            else:
                root_value = self._root_schema.adapt(root_value, inplace, path)

        # Catches AdaptationError and raises PartialAdaptationError if root
        # exists
        try:
            for k, v in new_obj.items():
                try:
                    adapter = self[k].adapt
                except KeyError:
                    raise errors.AdaptationError((None, path))
                else:
                    new_obj[k] = adapter(v, inplace, path + [k])
        except errors.AdaptationError as ex:
            if self.root_key is not None:
                raise errors.PartialAdaptationError(ex.args[0], ex)

        # Writes root key back to the dictionary
        if self.root_key is not None:
            new_obj[self.root_key] = root_value

        # Checks validity
        if self.is_valid(new_obj):
            if inplace:
                obj.update(new_obj)
                return obj
            else:
                return new_obj

    #===========================================================================
    # Magic methods: support the Mapping protocol
    #===========================================================================
    def __getitem__(self, key):
        try:
            return self._schemas[key]
        except KeyError as ex:
            if key is not None and key == self.root_key:
                raise ex
            else:
                return self._root_schema

    def __iter__(self):
        return iter(self._fields)

    def __len__(self):
        return len(self._schemas) + (0 if self.root_key is None else 1)

    #===========================================================================
    # Auxiliary methods
    #===========================================================================
    def add_item(self, key, schema):
        '''
        Register a schema for the given key.
        
        Example
        -------
        
        >>> from pyson.schema import *
        >>> schema = Object({'foo': Str('bar')})
        >>> schema['foo'].parent is schema
        True
        >>> schema['foo'].name
        u'foo'
        >>> schema['foo'].label
        u'Foo'
        '''

        if pyson_t.is_string(key):
            newvalue = self.as_child(schema)
            newvalue.name = key
            try:
                newvalue._ordering_index = schema._ordering_index
            except AttributeError:
                pass

            if key.endswith('?'):
                key = key[:-1]
                newvalue.is_optional = True
            if key.endswith('*'):
                key = key[:-1]
                newvalue.is_root = True

            if newvalue.is_root:
                if self.root_key is not None:
                    raise TypeError('object has two root values: %s and %s' % (self.root_key, key))
                self.root_key = key
                self._root_schema = newvalue
            else:
                self._schemas[key] = newvalue
        else:
            raise TypeError('invalid key of type %s' % type(key))

class Array(Container):
    INFO_ATTRIBUTES = Container.INFO_ATTRIBUTES + [ 'array_t' ]

    def __init__(self, array_t=Anything, *args, **kwds):
        '''
        Validator for list-like objects.
        
        Arguments
        ---------
        
        array_t : Schema
            Type of objects in array
         
         
        Examples
        --------
        
        >>> from pyson.schema import *
        >>> Array(Int).is_valid([])
        True
        >>> Array(Int).is_valid(['one', 'two'])
        False
        '''

        super(Array, self).__init__(*args, **kwds)
        self.array_t = self.as_child(array_t)

    def validate(self, obj, lazy=True, path=[]):
        if not pyson_t.is_array(obj):
            raise self.ValidationError(" %s object is not an Array" % type(obj))

        for idx, x in enumerate(obj):
            self.array_t.validate(x, lazy, path + [idx])

    def _expand_or_compress(self, is_expand, obj, **kwds):
        # Make a super call and disable validation
        # This will raise proper errors if obj is not valid and will guarantee
        # that if obj == null than obj is null. 
        obj = super(Array, self)._expand_or_compress(is_expand, obj, **kwds)
        kwds['validate'] = False

        if obj is self.null:
            return obj
        else:
            func = (self.type.expand if is_expand else self.type.compress)
            for i, item in enumerate(obj):
                obj[i] = func(item, **kwds)
            return obj

    def adapt(self, obj, inplace=False, path=[]):
        if not inplace:
            obj = list(obj)
        for idx, v in enumerate(obj):
            obj[idx] = self.array_t.adapt(v, inplace, path)
        return obj

# Save specialized _schemas into the Schema class
Schema.OBJECT_SCHEMA = Object
Schema.ARRAY_SCHEMA = Array

__all__ = get_schemas(globals())
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
