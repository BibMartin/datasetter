import pytest

from datasetter.dataset import Dataset


def test_dataframe():
    dataset = Dataset()
    assert dataset.metadata() == {'name': None,
                                  'description': None,
                                  'columns': None,
                                  'facets': None}

    with pytest.raises(NotImplementedError):
        dataset.count()

    with pytest.raises(NotImplementedError):
        dataset.count_by('facet')

    with pytest.raises(NotImplementedError):
        dataset.sample()
