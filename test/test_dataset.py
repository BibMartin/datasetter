import pytest
import numpy as np
import pandas as pd

from datasetter.dataset import Dataset, as_json


def test_as_json():
    assert as_json(None) is None
    assert as_json(pd.NaT) is None
    assert as_json(np.NaN) is None
    assert as_json({}) == {}
    assert isinstance(as_json(pd.Timestamp.utcnow()), str)


def test_dataframe():
    with pytest.raises(NotImplementedError):
        Dataset(pd.DataFrame(), [])

    with pytest.raises(NotImplementedError):
        Dataset.count(None)

    with pytest.raises(NotImplementedError):
        Dataset.count_by(None, 'facet')

    with pytest.raises(NotImplementedError):
        Dataset.sample(None)
