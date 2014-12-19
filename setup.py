#!/usr/bin/env python

from distutils.core import setup

setup(name='apt-py',
      version='0.1.0',
      description='apt reading and manipulating for python',
      author="David Sheldrick",
      package_dir={'apt': 'apt'},
      packages=['apt'])