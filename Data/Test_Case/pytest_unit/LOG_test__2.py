import numpy as np
from flojoy import OrderedPair, Vector, Scalar



def test_LOG_Vector_Scalar(mock_flojoy_decorator):
    import LOG

    x = Vector(v=np.arange(1, 11, 1))
    res = LOG.LOG(a=x, b=[Scalar(c=2)], log_base="input")
    test = np.log(x.v)
    test /= np.log(2)

    np.testing.assert_allclose(res.v, test)
