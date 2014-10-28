from pprint import pprint #@UnusedImport
from pyson.types import is_object, is_array

__all__ = ['indent', 'pprint', 'sprint', 'itemize']

def indent(st, indent=4, firstline=True, whitespace=' '):
    '''Indent string using ``indent`` whitespaces.
    
    Parameters
    ----------
    st : str or unicode
        String to be indented.
    indent : int
        Number of whitespace characters to be prepended to each line.
    firstline : bool
        If False, the first line will not be indented.
    whitespace : str
        A string representing the whitespace character. In most cases, it will
        be a space (' ') or a tab ('\t'), but any character is allowed.
        
    Examples
    --------
    
    >>> print(indent('foo:\\n--bar', whitespace='-'))
    ----foo:
    ------bar
    '''

    indent = whitespace * indent
    lines = st.splitlines()

    if firstline:
        return '\n'.join(indent + l for l in lines)
    else:
        return (indent + '\n').join(lines)

def itemize(strlist, bullet='* '):
    '''Format a list of strings using bullets to mark each item.
    
    Examples
    --------
    
    >>> print(itemize(['foo', 'bar', 'spam\\neggs']))
    * foo
    * bar
    * spam
      eggs
    '''
    lines = []
    ws = ' ' * len(bullet)
    for item in strlist:
        for idx, l in enumerate(item.splitlines()):
            if idx:
                lines.append(ws + l)
            else:
                lines.append(bullet + l)
    return '\n'.join(lines)

_indent_f = indent # to use in sprint implementation
def sprint(obj, indent=4, bullet='* '):
    '''
    Display JSON-like objects in a compact way. Differently to pretty print, it
    does not format objects using a valid dict/list syntax.
    
    Examples
    --------
    
    >>> obj = {'foo': {'foobar': 1, 'bar': 'null'}, 'bar': ['null', 1, 2, 3]} 
    >>> print(sprint(obj))
    bar:
        * null
        * 1
        * 2
        * 3
    foo:
        bar: null
        foobar: 1
    '''
    if is_object(obj):
        if obj:
            items = []
            obj_items = obj.items()
            obj_items.sort()
            for key, value in obj_items:
                if is_object(value) or is_array(value):
                    value = '\n' + _indent_f(sprint(value), indent)
                else:
                    value = ' ' + sprint(value)
                items.append('%s:%s' % (key, value))
            return '\n'.join(items)
        return '<empty>'
    elif is_array(obj):
        if obj:
            return itemize(map(sprint, obj))
        else:
            return '<empty>'
    else:
        data = unicode(obj)
        if '\n' in data:
            data = '\n' + _indent_f(data, indent)

        return data

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=0)
