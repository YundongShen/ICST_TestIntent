import numpy as np
from flojoy import OrderedPair, Vector, Scalar




def test_ADD_OrderedPair_Vector(mock_flojoy_decorator):
    import ADD

    x = np.arange(-10, 10, 1)
    y = np.arange(-20, 20, 2)
    z = np.arange(-30, 30, 3)
    res = ADD.ADD(a=OrderedPair(x=x, y=y), b=[Vector(v=z)])

    np.testing.assert_allclose(res.x, x)
    np.testing.assert_allclose(res.y, y + z)
