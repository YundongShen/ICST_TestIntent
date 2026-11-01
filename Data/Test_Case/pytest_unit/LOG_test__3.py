import numpy as np
from flojoy import OrderedPair, Vector, Scalar




def test_LOG_OrderedPair_Vector(mock_flojoy_decorator):
    import LOG

    x = np.arange(10, 20, 1)
    y = np.arange(20, 30, 1)
    z = np.arange(30, 40, 1)
    res = LOG.LOG(a=OrderedPair(x=x, y=y), b=[Vector(v=z)], log_base="input")
    test = np.log(y)
    test /= np.log(z)

    np.testing.assert_allclose(res.x, x)
    np.testing.assert_allclose(res.y, test)
