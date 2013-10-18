#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Radim Rehurek <radimrehurek@seznam.cz>

# TODO: check whether we should follow
# http://cffi.readthedocs.org/en/release-0.7/#distributing-modules-using-cffi
import os
import sys

from setuptools import Extension, setup

if sys.version_info < (2, 5):
    raise Exception('This version of sparsesvd needs Python 2.5 or later.')

sourcefiles = ['SVDLIBC/las2.c', 'SVDLIBC/svdutil.c', 'SVDLIBC/svdlib.c']


setup(
    name='sparsesvd-cffi',
    version='0.2.3-dev',
    description=(
        'Python module that wraps SVDLIBC, '
        'a library for sparse Singular Value Decomposition.'
    ),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ).read(),
    license='BSD',
    keywords='Singular Value Decomposition, SVD, sparse SVD',
    # there is a bug in python2.5, preventing distutils from using any
    # non-ascii characters :( http://bugs.python.org/issue2562
    author='Radim Rehurek',  # u'Radim Řehůřek', # <- should  be this...
    author_email='radimrehurek@seznam.cz',
    url='http://pypi.python.org/pypi/sparsesvd',
    download_url='http://pypi.python.org/pypi/sparsesvd',
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: BSD License',
    ],
    test_suite="test",
    install_requires=[
        'scipy >= 0.6.0',
        'cffi',
    ],
    py_modules=['sparsesvd'],
    ext_modules=[Extension('svdlib', sources=sourcefiles)]
)
