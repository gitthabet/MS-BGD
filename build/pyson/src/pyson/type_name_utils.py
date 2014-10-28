'''
Functions that map types to names (and vice versa) to be used by `jsonfy` and 
`unjsonfy` modules. 
'''

def type2name(cls):
    '''Return the full name of a type.
    
    Full name is composed by __module__.__name__, except for builtin types which
    is simply the type name.
    
    Examples
    --------
    
    >>> type2name(dict)
    'dict'
    >>> import datetime
    >>> type2name(datetime.date)
    'datetime.date'
    '''

    module = cls.__module__
    name = cls.__name__
    if module == '__builtin__':
        return name
    else:
        return '%s.%s' % (module, name)

def name2type(name):
    '''Return a type from its qualified name.
    
    Examples
    --------
    
    >>> name2type('random.Random')
    <class 'random.Random'>
    '''

    if '.' not in name:
        return getattr(__builtins__, name)
    else:
        mod, _, name = name.rpartition('.')
        mod = __import__(mod)
        return getattr(mod, name)

def load_modules(path):
    '''Tries to load all modules in the given path'''

    spath = path.split('.')
    current = ''
    for node in spath:
        current = node if not current else '%s.%s' % (current, node)
        try:
            __import__(current)
        except ImportError:
            break


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
