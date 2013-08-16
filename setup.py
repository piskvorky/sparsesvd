#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Radim Rehurek <radimrehurek@seznam.cz>

"""
Run with:

sudo python ./setup.py install
"""

import os
import sys

if sys.version_info[:2] < (2, 5):
    raise Exception('This version of sparsesvd needs Python 2.5 or later.')

sourcefiles = ['sparsesvd.pyx', 'SVDLIBC/las2.c', 'SVDLIBC/svdutil.c', 'SVDLIBC/svdlib.c']

def setup_package():
    META_DATA = dict(
        name = 'sparsesvd',
        version = '0.2.1',
        description = 'Python module that wraps SVDLIBC, a library for sparse Singular Value Decomposition.',
        long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
        license = 'BSD',
        keywords = 'Singular Value Decomposition, SVD, sparse SVD',
        # there is a bug in python2.5, preventing distutils from using any non-ascii characters :( http://bugs.python.org/issue2562
        author = 'Radim Rehurek', # u'Radim Řehůřek', # <- should really be this...
        author_email = 'radimrehurek@seznam.cz',
        url = 'http://pypi.python.org/pypi/sparsesvd',
        download_url = 'http://pypi.python.org/pypi/sparsesvd',
        zip_safe = False,
        platforms = 'any',
        include_package_data = True,
        entry_points = {},

        classifiers = [ # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
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

        test_suite = "test",

        install_requires = [
            'scipy >= 0.6.0',
            'cython',
        ],
    )

    if '--help' in sys.argv[1:] or \
      sys.argv[1] in ('--help-commands', 'egg_info', '--version'):
        pass
    else:
        import Cython  # NOQA
        # may need to work around setuptools bug by providing a fake Pyrex
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fake_pyrex"))

        import ez_setup
        ez_setup.use_setuptools()
        from setuptools import Extension

        from Cython.Distutils import build_ext
        from numpy.distutils.misc_util import get_numpy_include_dirs

        META_DATA['cmdclass'] = {'build_ext': build_ext}
        META_DATA['ext_modules'] = [Extension("sparsesvd", sourcefiles, include_dirs=get_numpy_include_dirs())]

    from setuptools import setup

    setup(**META_DATA)


if __name__ == '__main__':
    setup_package()
