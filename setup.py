from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourcefiles = ['sparsesvd.pyx', 'SVDLIBC/las2.c', 'SVDLIBC/svdutil.c', 'SVDLIBC/svdlib.c']

setup(
    name = 'sparsesvd',
    version = '0.1.9',
    description = 'Python module that wraps SVDLIBC, a library for sparse Singular Value Decomposition.',
    long_description = open('README.rst').read(),
    license = 'BSD',
    keywords = 'Singular Value Decomposition, SVD, sparse SVD',
    # there is a bug in python2.5, preventing distutils from using any non-ascii characters :( http://bugs.python.org/issue2562
    author = 'Radim Rehurek', # u'Radim Řehůřek', # <- should really be this...
    author_email = 'radimrehurek@seznam.cz',
    url = 'http://pypi.python.org/pypi/sparsesvd',
    download_url = 'http://pypi.python.org/pypi/sparsesvd',
    platforms = 'any',

    classifiers = [ # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: BSD License',
    ],

    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("sparsesvd", sourcefiles)],
)
