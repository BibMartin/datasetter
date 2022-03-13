import forge
from fastapi import HTTPException
from typing import Optional
import pandas as pd
import json
from datasetter.dataset import FacetUnavailableError


def as_json(doc):
    return json.loads(
        pd.Series([doc])
        .to_json(orient='records', date_format='iso')
        )[0]


def add_dataset(fast_api, uri, dataset):
    """Create FastAPI endpoints to serve the dataset.

    Parameters
    ----------
    fast_api : fastapi.applications.FastAPI
        A FastAPI application object. A new endpoint will be added in this application.
    uri : str
        The relative uri where the endpoint will be added.
    dataset : datasetter.dataset.Dataset
        The dataset object to be served.

    Returns
    -------
    Nothing : The endpoint is created as a side effect (inplace) in the `fast_api` application.
    """
    uri = '/' + uri.strip('/')
    facet = forge.kwarg('facet', type=str)
    rows = forge.kwarg('rows', default=10, type=Optional[int])
    skip = forge.kwarg('skip', default=0, type=Optional[int])
    kwargs = [forge.kwarg(facet, default=None, type=Optional[str])
              for facet in dataset.facets]

    @fast_api.get(uri + "/")
    def get_metadata():
        return as_json(dataset.metadata)

    @fast_api.get(uri + "/count")
    @forge.sign(*kwargs)
    def count(**kwargs):
        filters = {key: val for key, val in kwargs.items() if val is not None}
        count = dataset.count(**filters)
        return as_json({
            "count": int(count),
            "filters": filters,
            })

    @fast_api.get(uri + "/count-by/{facet}")
    @forge.sign(facet, rows, skip, *kwargs)
    def count_by(facet, rows=10, skip=0, **kwargs):
        filters = {key: val for key, val in kwargs.items() if val is not None}
        try:
            result = dataset.count_by(facet, rows=rows, skip=skip, **filters)
        except FacetUnavailableError:
            raise HTTPException(status_code=404,
                                detail="FacetUnavailableError: no facet {}".format(facet))
        return as_json({
            "facet": facet,
            # "count": len(result),  # TODO : add "nunique" feature in count_by schema
            "rows": len(result),
            "skip": skip,
            "filters": filters,
            "data": [{"value": str(key), "count": int(val)} for key, val in result.items()],
            })

    @fast_api.get(uri + "/sample")
    @forge.sign(rows, skip, *kwargs)
    def sample(rows=10, skip=0, **kwargs):
        filters = {key: val for key, val in kwargs.items() if val is not None}
        result = dataset.sample(rows=rows, skip=skip, **filters)
        count = dataset.count(**filters)
        return as_json({
            # "facet": facet,
            "count": count,
            "rows": len(result),
            "skip": skip,
            "filters": filters,
            "data": result.to_dict(orient='records'),
            })
