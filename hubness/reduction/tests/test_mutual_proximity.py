import pytest
from sklearn.datasets import make_classification
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_raises
from hubness.reduction import MutualProximity
from hubness.neighbors import NearestNeighbors

METHODS = ['normal', 'exact',
           ]
ALLOWED_METHODS = ['exact', 'empiric', 'normal', 'gaussi',
                   ]


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('verbose', [0, 1])
def test_mp_runs_without_error(method, verbose):
    X, y = make_classification(n_samples=20, n_features=10)
    nn = NearestNeighbors()
    nn.fit(X, y)
    neigh_dist, neigh_ind = nn.kneighbors()

    mp = MutualProximity(method=method, verbose=verbose)
    _ = mp.fit(neigh_dist, neigh_ind, assume_sorted=True).transform(neigh_dist, neigh_ind)


@pytest.mark.parametrize('method', ['invalid', None])
def test_invalid_method(method):
    X, y = make_classification(n_samples=10, )
    nn = NearestNeighbors()
    nn.fit(X, y)
    neigh_dist, neigh_ind = nn.kneighbors()

    mp = MutualProximity(method=method)
    with assert_raises(ValueError):
        mp.fit(neigh_dist, neigh_ind)