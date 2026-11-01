import numpy as np
from flojoy import OrderedPair, Vector, Scalar


def test_LOG_Vector_Vector(mock_flojoy_decorator):
    import LOG

    x = Vector(v=np.arange(10, 20, 1))
    y = Vector(v=np.arange(20, 30, 1))
    res = LOG.LOG(a=x, b=[y], log_base="input")
    test = np.log(x.v)
    test /= np.log(y.v)

    np.testing.assert_allclose(res.v, test)
