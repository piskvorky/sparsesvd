import os.path
import sysconfig

from scipy.sparse import isspmatrix_csc
import numpy as np

from cffi import FFI


ffi = FFI()

ffi.cdef(
    """
void free(void *ptr);

/******************************** Structures *********************************/
typedef struct smat *SMat;
typedef struct dmat *DMat;
typedef struct svdrec *SVDRec;

/* Harwell-Boeing sparse matrix. */
struct smat {
  long rows;
  long cols;
  long vals;     /* Total non-zero entries. */
  long *pointr;  /* For each col (plus 1), index of first non-zero entry. */
  long *rowind;  /* For each nz entry, the row index. */
  double *value; /* For each nz entry, the value. */
};

/* Row-major dense matrix.  Rows are consecutive vectors. */
struct dmat {
  long rows;
  long cols;
  double **value; /* Accessed by [row][col]. Free value[0] and value to free.*/
};

struct svdrec {
  int d;      /* Dimensionality (rank) */
  DMat Ut;    /* Transpose of left singular vectors. (d by m)
                 The vectors are the rows of Ut. */
  double *S;  /* Array of singular values. (length d) */
  DMat Vt;    /* Transpose of right singular vectors. (d by n)
                 The vectors are the rows of Vt. */
};

/* Performs the las2 SVD algorithm and returns the resulting Ut, S, and Vt. */
extern SVDRec svdLAS2(SMat A, long dimensions, long iterations, double end[2],
                      double kappa);
/* Chooses default parameter values.  Set dimensions to 0 for all dimensions: */
extern SVDRec svdLAS2A(SMat A, long dimensions);
  """
)

here = os.path.dirname(__file__)
lib = ffi.dlopen(os.path.join(here, "svdlib{}".format(sysconfig.get_config_var('EXT_SUFFIX'))))


def sparsesvd(matrix, k):
    if not isspmatrix_csc(matrix):
        raise TypeError("First argument must be a scipy.sparse.csc_matrix")

    k = int(k)

    mat = ffi.new('SMat')

    mat.rows = matrix.shape[0]
    mat.cols = matrix.shape[1]
    mat.vals = matrix.nnz

    indptr = np.ascontiguousarray(matrix.indptr, dtype=np.dtype('l'))
    indices = np.ascontiguousarray(matrix.indices, dtype=np.dtype('l'))
    data = np.ascontiguousarray(matrix.data, dtype=np.double)

    mat.pointr = ffi.cast("long *", indptr.ctypes.data)
    mat.rowind = ffi.cast("long *", indices.ctypes.data)
    mat.value = ffi.cast("double *", data.ctypes.data)

    srec = lib.svdLAS2A(mat, k)

    p_Ut = srec.Ut
    # An ugly and slow to covert void ** to a two dimensional array.
    Ut = np.array(list(list(r[0:p_Ut.cols]) for r in p_Ut.value[0:srec.d]))

    s = np.array(list(srec.S[0:srec.d]), copy=False)

    p_Vt = srec.Vt
    Vt = np.array(list(list(r[0:p_Vt.cols]) for r in p_Vt.value[0:srec.d]))

    # this was malloc'ed by svdLAS2A
    lib.free(srec.Ut.value)
    lib.free(srec.Ut)
    lib.free(srec.Vt)
    lib.free(srec.Vt.value)
    lib.free(srec)

    return Ut, s, Vt
