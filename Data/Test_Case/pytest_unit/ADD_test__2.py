import numpy as np
from flojoy import OrderedPair, Vector, Scalar



def test_ADD_Vector_Scalar(mock_flojoy_decorator):
    import ADD

    x = Vector(v=np.arange(-10, 10, 1))
    res = ADD.ADD(a=x, b=[Scalar(c=2), Scalar(c=3)])

    np.testing.assert_allclose(res.v, x.v + 2 + 3)
