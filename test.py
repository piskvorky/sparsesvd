import unittest
import sparsesvd
import scipy.sparse
import numpy

class TestSparseSVD(unittest.TestCase):
        def test_svd(self):
            m = numpy.arange(1500).reshape(30, 50)
            sm = scipy.sparse.csc_matrix(m, dtype = float)
            ut, s, vt = sparsesvd.sparsesvd(sm, 30)
            self.assertTrue(numpy.allclose(m, numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt))))
        
        def test_exception(self):
            m = 5
            self.assertRaises(TypeError, sparsesvd.sparsesvd, m, 3)


if __name__ == '__main__':
    unittest.main()

