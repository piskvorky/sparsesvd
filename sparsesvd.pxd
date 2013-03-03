cdef extern from "SVDLIBC/svdlib.h":
    ctypedef smat * SMat
    ctypedef dmat * DMat
    ctypedef svdrec * SVDRec

    struct smat:
        long rows, cols, vals, *pointr, *rowind
        double *value

    struct dmat:
        long rows, cols
        double **value

    struct svdrec:
        int d
        DMat Ut
        double *S
        DMat Vt

    SVDRec svdLAS2(SMat A, long dimensions, long iterations, double *end, double kappa)
    SVDRec svdLAS2A(SMat A, long dimensions)
