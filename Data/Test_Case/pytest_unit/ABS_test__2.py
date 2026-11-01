import numpy as np
from flojoy import Scalar, Vector, OrderedPair


# Test for Scalar, Vector and OrderedPair



def test_ABS_vector(mock_flojoy_decorator):
    import ABS

    x = Vector(v=np.arange(-10, 10, 1))
    res = ABS.ABS(default=x)

    np.testing.assert_allclose(res.x, x.v)
    np.testing.assert_allclose(res.y, np.abs(x.v))
