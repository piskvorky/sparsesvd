# cython: infer_types=True

from scipy.sparse import issparse, isspmatrix_csc
cimport numpy as np
import numpy as np
from libc.stdlib cimport free

def sparsesvd(matrix, k):
    if not isspmatrix_csc(matrix):
        raise TypeError("First argument must be a scipy.sparse.csc_matrix")
    k = int(k)

    cdef SVDRec srec
    cdef smat mat

    mat.rows = matrix.shape[0]
    mat.cols = matrix.shape[1]
    mat.vals = matrix.nnz

    """
    # old style
    cdef np.ndarray[long, mode = 'c'] indptr = np.ascontiguousarray(matrix.indptr, dtype=np.long)
    cdef np.ndarray[long, mode = 'c'] indices = np.ascontiguousarray(matrix.indices, dtype=np.long)
    cdef np.ndarray[double, mode = 'c'] data = np.ascontiguousarray(matrix.data, dtype=np.double)
    mat.pointr = <long *>indptr.data
    mat.rowind = <long *>indices.data
    mat.value = <double *>data.data
    """

    cdef long [:] indptr = np.ascontiguousarray(matrix.indptr, dtype=np.dtype('l'))
    cdef long [:] indices = np.ascontiguousarray(matrix.indices, dtype=np.dtype('l'))
    cdef double [:] data = np.ascontiguousarray(matrix.data, dtype=np.double)
    mat.pointr = &indptr[0]
    mat.rowind = &indices[0]
    mat.value = &data[0]

    srec = svdLAS2A(&mat, k)

    p_Ut = <double[:srec.d, :srec.Ut.cols]> srec.Ut.value[0]
    p_Ut.callback_free_data = free
    Ut = np.array(p_Ut, copy=False)

    p_Vt = <double[:srec.d, :srec.Vt.cols]> srec.Vt.value[0]
    p_Vt.callback_free_data = free
    Vt = np.array(p_Vt, copy=False)

    p_s = <double[:srec.d]> srec.S
    p_s.callback_free_data = free
    s = np.array(p_s, copy=False)

    # this was malloc'ed by svdLAS2A
    free(srec.Ut.value)
    free(srec.Ut)
    free(srec.Vt)
    free(srec.Vt.value)
    free(srec)

    return Ut, s, Vt
