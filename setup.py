#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Radim Rehurek <radimrehurek@seznam.cz>

"""
Run with:

sudo python ./setup.py install
"""

import os
import sys

if sys.version_info[:2] < (2, 5):
    raise Exception('This version of gensim needs Python 2.5 or later. ')

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, Extension

from numpy.distutils.misc_util import get_numpy_include_dirs



module = Extension('sparsesvd',
                    extra_compile_args = ['-std=c99'],
                    include_dirs = get_numpy_include_dirs(),
                    sources = ['sparsesvdmodule.c', 'SVDLIBC/las2.c', 'SVDLIBC/svdlib.c', 'SVDLIBC/svdutil.c'])


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_desc = read('README.rst')



setup(
    name = 'sparsesvd',
    version = '0.1.7',
    description = 'Python module that wraps SVDLIBC, a library for sparse Singular Value Decomposition.',
    long_description = long_desc,
    license = 'BSD',
    keywords = 'Singular Value Decomposition, SVD, sparse SVD',
    # there is a bug in python2.5, preventing distutils from using any non-ascii characters :( http://bugs.python.org/issue2562
    author = 'Radim Rehurek', # u'Radim Řehůřek', # <- should really be this...
    author_email = 'radimrehurek@seznam.cz',
    url = 'http://pypi.python.org/pypi/sparsesvd',
    download_url = 'http://pypi.python.org/pypi/sparsesvd',
    zip_safe = False,
    platforms = 'any',

    classifiers = [ # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: BSD License',
    ],

    test_suite = "test",

    install_requires = [
        'scipy >= 0.6.0',
    ],

    include_package_data = True,

    entry_points = {},

    ext_modules = [module],

)
