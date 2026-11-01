import numpy as np
from flojoy import OrderedPair, Vector, Scalar


def test_ADD_Vector_Vector(mock_flojoy_decorator):
    import ADD

    x = Vector(v=np.arange(-10, 10, 1))
    y = Vector(v=np.arange(-20, 20, 2))
    res = ADD.ADD(a=x, b=[y])

    np.testing.assert_allclose(res.v, x.v + y.v)
