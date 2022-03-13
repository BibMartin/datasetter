# import pytest
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.testclient import TestClient

from datasetter.utils import doc_equal
from datasetter.api import as_json, add_dataset
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

dataset = PandasDataset(df, ['letter', 'greek'], metadata=metadata)

app = FastAPI()
add_dataset(app, 'pandas-dataset', dataset)
# Launch app from parent directory with:
# > uvicorn test.test_api:app --host 0.0.0.0 --port 8000 --reload

client = TestClient(app)


def test_as_json():
    assert as_json(None) is None
    assert as_json(pd.NaT) is None
    assert as_json(np.NaN) is None
    assert as_json({}) == {}
    assert isinstance(as_json(pd.Timestamp.utcnow()), str)


def test_metadata():
    r = client.get('/pandas-dataset/')
    assert r.status_code == 200
    assert doc_equal(r.json(), metadata)


def test_count():
    r = client.get('/pandas-dataset/count')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': 9, 'filters': {}})

    r = client.get('/pandas-dataset/count?letter=A')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': 3, 'filters': {'letter': 'A'}})

    r = client.get('/pandas-dataset/count',
                   params=dict(letter='A', greek='alpha'))
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': 1, 'filters': {'letter': 'A', 'greek': 'alpha'}})


def test_count_by():
    r = client.get('/pandas-dataset/count-by/letter')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'facet': 'letter',
         'rows': 4,
         'skip': 0,
         'filters': {},
         'data': [
             {'value': 'A', 'count': 3},
             {'value': 'B', 'count': 2},
             {'value': 'C', 'count': 2},
             {'value': 'D', 'count': 2}]})

    r = client.get('/pandas-dataset/count-by/greek')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'facet': 'greek',
         'rows': 3,
         'skip': 0,
         'filters': {},
         'data': [
             {'value': 'alpha', 'count': 3},
             {'value': 'beta', 'count': 3},
             {'value': 'gamma', 'count': 3}]})

    r = client.get('/pandas-dataset/count-by/foo')
    assert r.status_code == 404
    assert doc_equal(
        r.json(),
        {'detail': 'FacetUnavailableError: no facet foo'})

    r = client.get('/pandas-dataset/count-by/number')
    assert r.status_code == 404
    assert doc_equal(
        r.json(),
        {'detail': 'FacetUnavailableError: no facet number'})


def test_sample():
    r = client.get('/pandas-dataset/sample')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': min(10, dataset.count()),
         'rows': min(10, dataset.count()),
         'skip': 0,
         'filters': {},
         'data': df.to_dict(orient='records')})

    r = client.get('/pandas-dataset/sample?rows=3')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': min(10, dataset.count()),
         'rows': min(3, dataset.count()),
         'skip': 0,
         'filters': {},
         'data': df.head(3).to_dict(orient='records')})

    r = client.get('/pandas-dataset/sample?letter=A')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': min(10, dataset.count(letter="A")),
         'rows': min(3, dataset.count(letter="A")),
         'skip': 0,
         'filters': {'letter': 'A'},
         'data': dataset.sample(letter='A').to_dict(orient='records')})

    r = client.get('/pandas-dataset/sample?letter=A&rows=2')
    assert r.status_code == 200
    assert doc_equal(
        r.json(),
        {'count': dataset.count(letter="A"),
         'rows': min(2, dataset.count(letter="A")),
         'skip': 0,
         'filters': {'letter': 'A'},
         'data': (dataset.sample(letter='A').head(2)
                  .to_dict(orient='records'))})
