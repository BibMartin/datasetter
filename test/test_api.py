# import pytest
import numpy as np
import pandas as pd

from datasetter.api import as_json


def test_as_json():
    assert as_json(None) is None
    assert as_json(pd.NaT) is None
    assert as_json(np.NaN) is None
    assert as_json({}) == {}
    assert isinstance(as_json(pd.Timestamp.utcnow()), str)
