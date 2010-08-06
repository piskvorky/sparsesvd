=================================================
sparsesvd -- Sparse Singular Value Decomposition
=================================================

**sparsesvd** is a Python wrapper around `SVDLIBC <http://tedlab.mit.edu/~dr/SVDLIBC/>`_ 
library by Doug Rohde, which is itself based on `SVDPACKC <http://www.netlib.org/svdpack/>`_ by Michael Berry.

sparsesvd uses SciPy's sparse CSC (Compressed Sparse Column) matrix format as input to SVD.
This is the same format used internally by SVDLIBC, so that no extra data copies need to be
made by the Python wrapper. 

Installation
------------

You'll need NumPy and Scipy, two Python packages for scientific computing.
You need to have them installed prior to installing sparsesvd; if you don't have them yet, 
you can get them from <http://www.scipy.org/Download>.

The simple way to install `sparsesvd` is::

    sudo easy_install sparsesvd

Or, if you have instead downloaded and unzipped the `source tar.gz <http://pypi.python.org/pypi/sparsesvd>`_ package, 
you'll need to run::

    python setup.py test
    sudo python setup.py install

This version has been tested under Python 2.5, but should run on any 2.5 <= Python < 3.0.

Documentation
--------------

The `sparsesvd` module offers a single function, `sparsesvd`, which accepts two parameters.
One is a sparse matrix in the `scipy.sparse.csc_matrix` format, the other is the number
of requested factors (an integer).

>>> import numpy, scipy.sparse
>>> from sparsesvd import sparsesvd
>>> mat = numpy.random.rand(200, 100)
>>> ut, s, vt = sparsesvd(scipy.sparse.csc_matrix(mat), 100)
>>> assert numpy.allclose(mat, numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt)))


-------

Original wrapper by Lubos Kardos, package maintained by Radim Rehurek.