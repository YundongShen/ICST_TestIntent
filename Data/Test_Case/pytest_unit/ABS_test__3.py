import numpy as np
from flojoy import Scalar, Vector, OrderedPair


# Test for Scalar, Vector and OrderedPair




def test_ABS_OrderedPair(mock_flojoy_decorator):
    import ABS

    x = np.arange(-10, 10, 1)
    y = np.arange(-20, 20, 1)
    res = ABS.ABS(default=OrderedPair(x=x, y=y))

    np.testing.assert_allclose(res.x, x)
    np.testing.assert_allclose(res.y, np.abs(y))
