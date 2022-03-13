import pytest
import pandas as pd

from datasetter.dataset import FacetUnavailableError
from datasetter.pandas_dataset import PandasDataset


df = pd.DataFrame([
    ['A', 'alpha', 1],
    ['A', 'beta', 13],
    ['A', 'gamma', 8],
    ['B', 'alpha', 1],
    ['B', 'beta', 31],
    ['C', 'gamma', 9],
    ['C', 'alpha', 2],
    ['D', 'beta', 21],
    ['D', 'gamma', 0],
    ], columns=['letter', 'greek', 'number'])

metadata = {
    "description": "A simple dataset to make tests.",
    "facets": ['letter', 'greek'],
    "columns": [
        {"name": "letter", "type": "string", "description": "A column with letters."},
        {"name": "greek", "type": "string", "description": "A column with greek letters."},
        {"name": "number", "type": "integer", "description": "A column with numbers."},
        ]}

dataset = PandasDataset(df, **metadata)


def test_count():
    assert dataset.count() == 9
    assert dataset.count(letter="A") == 3
    assert dataset.count(letter="A", greek="alpha") == 1

    with pytest.raises(FacetUnavailableError):
        dataset.count(foo=3)

    with pytest.raises(FacetUnavailableError):
        dataset.count(number=3)


def test_count_by():
    assert (dataset.count_by('letter') == pd.Series({"A": 3, "B": 2, "C": 2, "D": 2})).all()

    assert (dataset.count_by('greek') == pd.Series({"alpha": 3, "beta": 3, "gamma": 3})).all()

    with pytest.raises(FacetUnavailableError):
        dataset.count_by('foo')

    with pytest.raises(FacetUnavailableError):
        dataset.count_by('number')


def test_sample():
    assert len(dataset.sample(rows=3)) == 3

    assert len(dataset.sample()) == min(10, dataset.count())

    assert len(dataset.sample(letter='A')) == 3

    assert len(dataset.sample(rows=2, letter='A')) == 2

    with pytest.raises(FacetUnavailableError):
        dataset.sample(foo=12)

    with pytest.raises(FacetUnavailableError):
        dataset.sample(number=12)
