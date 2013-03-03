=================================================
sparsesvd -- Sparse Singular Value Decomposition
=================================================

**sparsesvd** is a Python wrapper around the `SVDLIBC <http://tedlab.mit.edu/~dr/SVDLIBC/>`_
library by Doug Rohde, which is itself based on Michael Berry's `SVDPACK <http://www.netlib.org/svdpack/>`_.

sparsesvd uses SciPy's sparse CSC (Compressed Sparse Column) matrix format as input to SVD.
This is the same format used internally by SVDLIBC, so that no extra data copies need to be
made by the Python wrapper (memory-efficient).

Installation
------------

In order to install `sparsesvd`, you'll need NumPy, Scipy and Cython.

Install `sparsesvd` and its dependencies with::

    pip install numpy
    pip install scipy
    pip install cython
    pip install sparsesvd

In case of problems, see `<http://www.scipy.org/Download>`_ for instructions on installing
SciPy on various platforms.

If you have instead downloaded and unzipped the `source tar.gz <http://pypi.python.org/pypi/sparsesvd>`_ package, run::

    python setup.py test
    sudo python setup.py install

This version has been tested under Python 2.6 and 3.2, but should run on any
later versions of both 2.x and 3.x series.

Documentation
--------------

The `sparsesvd` module offers a single function, `sparsesvd`, which accepts two parameters.
One is a sparse matrix in the `scipy.sparse.csc_matrix` format, the other the number
of requested factors (an integer):

>>> import numpy, scipy.sparse
>>> from sparsesvd import sparsesvd
>>> mat = numpy.random.rand(200, 100) # create a random matrix
>>> smat = scipy.sparse.csc_matrix(mat) # convert to sparse CSC format
>>> ut, s, vt = sparsesvd(smat, 100) # do SVD, asking for 100 factors
>>> assert numpy.allclose(mat, numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt)))


-------

Original wrapper by Lubos Kardos, package updated and maintained by Radim Rehurek, Cython and Python 3.x port by Alejandro Pulver. For an application of sparse SVD to Latent Semantic Analysis, see the `gensim <http://pypi.python.org/pypi/gensim>`_ package.

You can use this code under the `simplified BSD license <http://www.opensource.org/licenses/bsd-license.php>`_.
