import numpy as np
from pgvector.utils import SparseVector
import pytest
from scipy.sparse import coo_array


class TestSparseVector:
    def test_from_list(self):
        vec = SparseVector([1, 0, 2, 0, 3, 0])
        assert vec.to_list() == [1, 0, 2, 0, 3, 0]
        assert vec.to_numpy().tolist() == [1, 0, 2, 0, 3, 0]

    def test_from_list_dimensions(self):
        with pytest.raises(ValueError) as error:
            SparseVector([1, 0, 2, 0, 3, 0], 6)
        assert str(error.value) == 'dimensions not allowed'

    def test_from_numpy(self):
        assert SparseVector(np.array([1, 0, 2, 0, 3, 0])).to_list() == [1, 0, 2, 0, 3, 0]

    def test_from_dict(self):
        vec = SparseVector({2: 2, 4: 3, 0: 1, 3: 0}, 6)
        assert vec.to_list() == [1, 0, 2, 0, 3, 0]
        assert vec.indices() == [0, 2, 4]

    def test_from_dict_no_dimensions(self):
        with pytest.raises(ValueError) as error:
            SparseVector({0: 1, 2: 2, 4: 3})
        assert str(error.value) == 'dimensions required'

    def test_from_scipy(self):
        arr = coo_array(np.array([1, 0, 2, 0, 3, 0]))
        assert SparseVector(arr).to_list() == [1, 0, 2, 0, 3, 0]
        assert SparseVector(arr.todok()).to_list() == [1, 0, 2, 0, 3, 0]

    def test_from_scipy_dimensions(self):
        with pytest.raises(ValueError) as error:
            SparseVector(coo_array(np.array([1, 0, 2, 0, 3, 0])), 6)
        assert str(error.value) == 'dimensions not allowed'

    def test_repr(self):
        assert repr(SparseVector([1, 0, 2, 0, 3, 0])) == 'SparseVector({0: 1.0, 2: 2.0, 4: 3.0}, 6)'
        assert str(SparseVector([1, 0, 2, 0, 3, 0])) == 'SparseVector({0: 1.0, 2: 2.0, 4: 3.0}, 6)'

    def test_dimensions(self):
        assert SparseVector([1, 0, 2, 0, 3, 0]).dimensions() == 6

    def test_indices(self):
        assert SparseVector([1, 0, 2, 0, 3, 0]).indices() == [0, 2, 4]

    def test_values(self):
        assert SparseVector([1, 0, 2, 0, 3, 0]).values() == [1, 2, 3]

    def test_to_coo(self):
        assert SparseVector([1, 0, 2, 0, 3, 0]).to_coo().toarray().tolist() == [[1, 0, 2, 0, 3, 0]]
