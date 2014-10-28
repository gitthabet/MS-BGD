from pyson import as_path, as_str_path

class SchemaError(ValueError):
    '''Base exception raised by schema operations.'''

    def __init__(self, *args):
        '''Raised when something goes wrong with a schema operation (validation, 
        adaptation, etc). SchemaError instances have an additional 'path' 
        attribute that describe the path in which the error occurred.
    
        When initialized with no arguments, all attributes will be empty. If 
        the first attribute is a 2-tuple, it will be interpreted as 
        (message, path). Otherwise, it is interpreted as a message. 
        
        >>> e = SchemaError(('msg', '$.path'))
        >>> e.message, e.args, e.path
        ('msg', (('msg', '$.path'),), ['path'])
        
        If message is None, it construct a more useful default message

        >>> e = SchemaError((None, '$.path'))
        >>> e.message, e.args, e.path
        ('on key %(path)s', ((None, '$.path'),), ['path'])

        SchemaError() cannot be initialized with more than 1 argument.        
        '''

        super(SchemaError, self).__init__(*args)

        if len(args) > 1:
            raise TypeError('SchemaError accepts at most 1 positional argument')

        if not args:
            self.path = None

        else:
            if isinstance(args[0], tuple) and len(args[0]) == 2:
                self.message = args[0][0]
                self.path = as_path(args[0][1])
            else:
                self.path = None

        if self.message is None and self.path is not None:
            self.message = self.make_message()


    def make_message(self):
        return 'on key %(path)s'

    @property
    def str_path(self):
        if self.path is None:
            return None
        else:
            result = as_str_path(self.path)
            try:
                return str(result)
            except:
                return result

    def __str__(self):
        return self.message % {'path': self.str_path}

    def __unicode__(self):
        return unicode(str(self))

class PartialError(SchemaError):
    '''Class to flag partial errors'''
    def __init__(self, arg, ex=None):
        if ex is None:
            if isinstance(arg, PartialError):
                arg, ex = arg.args
            elif isinstance(arg, SchemaError):
                ex, arg = arg, arg.args
            elif isinstance(arg, Exception):
                arg, ex = (), arg
        if isinstance(arg, tuple) and len(arg) == 1:
            arg = arg[0]

        super(PartialError, self).__init__(arg)
        self.args = (self.args, ex)
        self.exception = ex

    def __str__(self):
        base = super(PartialError, self).__str__()
        return '%s: %s' % (base, self.exception)

class ValidationError(SchemaError):
    '''Exception raised when object does not validate.'''

class PartialValidationError(PartialError, ValidationError):
    '''Error is raised when a root field validates, but not the whole object.'''

class MissingKeyError(ValidationError):
    '''Exception raised when dictionary misses required keys'''
    def make_message(self):
        return 'missing key: %(path)s'

class InvalidKeyError(ValidationError):
    '''Exception raised when invalid keys are found in dictionaries'''
    def make_message(self):
        return 'invalid key: %(path)s'

class ValidationIndexError(ValidationError):
    '''Invalid indexes in arrays'''

class AdaptationError(SchemaError):
    '''Errors when adapting objects to schemas'''

class PartialAdaptationError(PartialError, SchemaError):
    '''Errors when adapting objects to schemas'''

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)

