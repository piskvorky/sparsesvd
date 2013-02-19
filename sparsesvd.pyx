# cython: infer_types=True
from scipy.sparse import issparse, isspmatrix_csc
cimport numpy as np
import numpy as np
from libc.stdlib cimport free
from cython cimport view

def sparsesvd(matrix, k):
    if isspmatrix_csc(matrix):
        pass
    elif issparse(matrix):
        matrix = matrix.tocsc()
    else:
        raise TypeError("sparsesvd is for sparse matrices, see scipy.sparse")

    cdef SVDRec srec
    cdef smat mat

    mat.rows = matrix.shape[0]
    mat.cols = matrix.shape[1]
    mat.vals = matrix.nnz
    cdef np.ndarray[long, mode = 'c'] indptr = np.ascontiguousarray(matrix.indptr, dtype=np.long)
    cdef np.ndarray[long, mode = 'c'] indices = np.ascontiguousarray(matrix.indices, dtype=np.long)
    cdef np.ndarray[double, mode = 'c'] data = np.ascontiguousarray(matrix.data, dtype=np.double)
    #cdef double [:] data = np.ascontiguousarray(matrix.data, dtype=np.double)
    # TODO: type corversion may be needed?
    #cdef double [:] data = matrix
    mat.pointr = <long *>indptr.data
    mat.rowind = <long *>indices.data
    mat.value = <double *>data.data
    #mat.value = &data[0]

    srec = svdLAS2A(&mat, k)
    #cdef view.array Ut = view.array()
    #Ut.data = srec.Ut.value[0]
    #Ut.callback_free_data = free
    Ut = <double[:srec.d, :srec.Ut.cols]> srec.Ut.value[0]
    Ut.callback_free_data = free
    _Ut = np.array(Ut, copy=False)

    Vt = <double[:srec.d, :srec.Vt.cols]> srec.Vt.value[0]
    Vt.callback_free_data = free
    _Vt = np.array(Vt, copy=False)

    s = <double[:srec.d]> srec.S
    s.callback_free_data = free
    _s = np.array(s, copy=False)

    free(srec.Ut.value)
    free(srec.Ut)
    free(srec.Vt)
    free(srec.Vt.value)
    free(srec)

    return (_Ut, _s, _Vt)
