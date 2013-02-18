#!/usr/bin/env python

import re
from distutils.core import setup

setup(name='django-conceptq',
      version='0.1.1',
      description='Tiny query wrapper for composable, cross-relation complex queries.',
      long_description=re.sub("\.\. code-block :: python", "::", open('README.rst').read()),
      author='Charlie DeTar',
      author_email='cfd@media.mit.edu',
      url='https://github.com/yourcelf/conceptq',
      packages=['conceptq'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
