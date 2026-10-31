import numpy as np
from flojoy import Scalar, Vector, OrderedPair


# Test for Scalar, Vector and OrderedPair


def test_ABS_Scalar(mock_flojoy_decorator):
    import ABS

    res = ABS.ABS(default=Scalar(c=-1.0))

    assert res.x == -1.0
    assert res.y == 1.0
