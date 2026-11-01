import numpy as np

from flojoy import Vector


def test_POPULATE_array_value_uniform(mock_flojoy_decorator):
    import POPULATE

    x = Vector(v=np.arange(0, 99, 2))
    res = POPULATE.POPULATE(
        default=x, distribution="uniform", lower_bound=0, upper_bound=1
    )
    assert np.all(res.x == x.v)
    assert np.all(res.y < 1)
    assert np.all(res.y > 0)
