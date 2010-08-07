
#include <Python.h>
#include <numpy/arrayobject.h>

#include "SVDLIBC/svdlib.h"


static PyArrayObject *createPyArray2d(double* data, int rows, long cols)  {
    npy_intp dims[2];
    dims[0] = (npy_intp) rows;
    dims[1] = (npy_intp) cols;
    PyArrayObject* pyArray = (PyArrayObject*) PyArray_SimpleNewFromData(2, dims, NPY_FLOAT64, data);

    /* HACK: setting OWN_DATA flag will cause correct deallocation during pyArray 
     * object's destruction. *But* for this to work, the array must be allocated
     * with the same allocator as that in NumPy, so that allocator/deallocator matches.
     * 
     * Currently both NumPy and SVDLIBC use malloc, so it's ok. */
    pyArray->flags |= NPY_OWNDATA;
    return pyArray;
}


static PyArrayObject *createPyArray1d(double* data, int count) {
    npy_intp dims[] = {(npy_intp) count};
    PyArrayObject* pyArray = (PyArrayObject*)PyArray_SimpleNewFromData(1, dims, NPY_FLOAT64, data);
    pyArray->flags |= NPY_OWNDATA;
    return pyArray;
}


static PyObject *sparsesvd_sparsesvd(PyObject *self, PyObject *args) {   
    PyObject *matrix = NULL;
    long dimensions;
    if(!PyArg_ParseTuple(args, "Ol", &matrix, &dimensions))
        return NULL;
    if (strcmp(matrix->ob_type->tp_name, "csc_matrix") != 0)
    {
        PyErr_SetString(PyExc_TypeError, "First argument must be a csc_matrix");
        return NULL;
    }

    
    /* Create matrix representation for SVDLIBC; use array references wherever 
     * possible and copy arrays when not possible (input matrix not in doubles, etc.)
     */
    SMat m = (SMat) malloc(sizeof(struct smat));
    if(!m) {
        PyErr_NoMemory();
        return NULL;
    }
    
    // Retrieve matrix shape and density
    PyObject *shape = PyObject_GetAttrString(matrix, "shape");
    PyObject *rowsO = PySequence_GetItem(shape, 0);
    PyObject *colsO = PySequence_GetItem(shape, 1);
    long rows = PyInt_AsLong(rowsO);
    long cols = PyInt_AsLong(colsO);
    Py_DECREF(shape);
    Py_DECREF(rowsO);
    Py_DECREF(colsO);

    // Get raw data arrays from input matrix
    PyObject *dataT = PyObject_GetAttrString(matrix, "data");
    PyObject *indicesT = PyObject_GetAttrString(matrix, "indices");
    PyObject *indptrT = PyObject_GetAttrString(matrix, "indptr");
    
    /* Convert raw arrays to data types understood by SVDLIBC; only juggle around
     * pointers if already contiguous and of the right data type (most common case).
     */
    PyArrayObject *data = (PyArrayObject *)PyArray_FROM_OTF(dataT, PyArray_DOUBLE, NPY_CONTIGUOUS);
    Py_DECREF(dataT); // py object no longer needed
    PyArrayObject *indices = (PyArrayObject *)PyArray_FROM_OTF(indicesT, PyArray_LONG, NPY_CONTIGUOUS);
    Py_DECREF(indicesT);
    PyArrayObject *indptr = (PyArrayObject *)PyArray_FROM_OTF(indptrT, PyArray_LONG, NPY_CONTIGUOUS);
    Py_DECREF(indptrT);

    // Number of nonzero elements in the input matrix
    int nnz = PyArray_DIM(data, 0);

    m->rows = rows;
    m->cols = cols;
    m->vals = nnz;
    m->pointr = (long*)PyArray_DATA(indptr);
    m->rowind = (long*)PyArray_DATA(indices);
    m->value = (double*)PyArray_DATA(data);
    
    // call SVDLIBC's svdLAS2A
    SVDRec svdResult = svdLAS2A(m, dimensions);
    free(m);
    Py_DECREF(indptr);
    Py_DECREF(indices);
    Py_DECREF(data);
    
    if (svdResult == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "svdLAS2: fatal error, aborting");
        return NULL;
    }
    
    // Convert result to PyArrayObjects
    PyArrayObject* ut = createPyArray2d(svdResult->Ut->value[0], svdResult->d, svdResult->Ut->cols);
    PyArrayObject* vt = createPyArray2d(svdResult->Vt->value[0], svdResult->d, svdResult->Vt->cols);
    PyArrayObject* s = createPyArray1d(svdResult->S, svdResult->d);
    
    /* Memory deallocation handled by the returned arrays; the svdResult->Ut->value[0], 
     * svdResult->Vt->value[0] and svdResult->S arrays change ownership to ut, vt and s
     */
    free(svdResult->Ut->value);
    free(svdResult->Ut);
    free(svdResult->Vt->value);
    free(svdResult->Vt);
    free(svdResult);
    
    // Return as 3-tuple
    return Py_BuildValue("NNN", ut, s, vt);
}


static PyMethodDef sparsesvdMethods[] = {
    {"sparsesvd", (PyCFunction)sparsesvd_sparsesvd, METH_VARARGS,
        "sparsesvd(smat, dimensions)"
        "\n\nPerform partial sparse SVD of scipy.sparse.csc_matrix `smat` and return `ut`, `s`, `vt` such that `ut.T * s * vt ~= smat`."
        " Return only `dimensions` singular triplets that correspond to the greatest singular values (i.e., not necessarily the full spectrum)."
        "\n\nThis function uses the LAS2 algorithm from SVDLIBC, which solves the related sparse eigenproblem of `smat.T*smat` or `smat*smat.T` (whichever is more efficient)."
    },
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initsparsesvd(void) {
    (void) Py_InitModule("sparsesvd", sparsesvdMethods);
    import_array();
}
