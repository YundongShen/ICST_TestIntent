import numpy as np

from flojoy import Vector




def test_POPULATE_array_value_poisson(mock_flojoy_decorator):
    import POPULATE

    x = Vector(v=np.arange(0, 100000, 1))
    res = POPULATE.POPULATE(default=x, distribution="poisson", poisson_events=1)
    assert np.all(res.x == x.v)
    assert res.y.shape == x.v.shape
    assert abs(np.mean(res.y) - 1) < 0.015
