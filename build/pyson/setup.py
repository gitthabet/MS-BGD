#-*- coding: utf8 -*-
from distutils.core import setup
import os

# Save version file for documentation and for program
VERSION = '0.2'
with open(os.path.join('doc', 'source', 'VERSION'), 'w') as F:
    F.write(VERSION)
with open(os.path.join('src', 'pyson', 'version.py'), 'w') as F:
    F.write('VERSION = "%s"' % VERSION)

setup(name='pyson',
      version=VERSION,
      description='Maniplates JSON-like structures consisting of dictionaries and lists.',
      author='Fábio Macêdo Mendes',
      author_email='fabiomacedomendes@gmail.com',
      url='code.google.com/p/py-pyson',
      long_description=('pyson is a Python library for manipulating JSON-like'
                        ' data structures. It has support for schemas and'
                        ' validation, searching and querying, differences,'
                        ' iteration over JSON-like structures, and more'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries',
          ],
      package_dir={ '': 'src' },
      packages=['pyson', 'pyson.converter', 'pyson.iface', 'pyson.schema', 'pyson.types'],
      requires=['simplejson', 'propertylib'],
)
