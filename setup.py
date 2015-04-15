#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
#-----------------------------------------------------------------------------

from setuptools import setup
from io import open

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

version = {}
with open('simcx/__version__.py', encoding='utf-8') as f:
    exec(f.read(), version)

setup(
    name='simcx',
    version=version['__version__'],
    description='Simulation Framework for Complex Systems',
    long_description = long_description,
    url='none',
    author='Tiago Baptista',
    author_email='baptista@dei.uc.pt',
    packages=['simcx'],
    install_requires = ['pyglet', 'matplotlib', 'numpy', 'scipy'],
    license='LICENSE.txt'
)