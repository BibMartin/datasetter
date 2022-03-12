# Dataset : base class for datasetter

from typing import Optional
import pandas as pd
import json


def as_json(doc):
    return json.loads(
        pd.Series([doc])
        .to_json(orient='records', date_format='iso')
        )[0]


class Dataset(object):
    def __init__(self, dataframe, facets, metadata=None):
        # self._data = dataframe
        # self.facets = facets
        # self.metadata = metadata
        raise NotImplementedError()

    def count(self, **filters):
        """Counts the number of records in the Dataset.

        Parameters
        ----------
        **filters : key-value mapping.
            Values you want to filter on. Keys must be part of self.facets.

        Returns
        -------
        count : int
            Number of records found.
        """
        raise NotImplementedError()

    def count_by(self, facet, rows=10, skip=0, **filters):
        """Provides a sample of one facet's values.

        Parameters
        ----------
        facet : str
            The name of the facet you want to list. It must be part of self.facets
        rows : int, default 10
            The maximal number of rows returned.
        skip : int, default 0
            The number of rows to skip before returning (for pagination).
        **filters : key-value mapping (Not implemented)
            Values you want to filter on. Keys must be part of self.facets.

        Returns
        -------
        sample : Series
            A histogram of the facet data.
        """
        raise NotImplementedError()

    def sample(self, rows=10, skip=0, **filters):
        """Provides a sample from the dataset.

        Parameters
        ----------
        rows : int, default 10
            The maximal number of rows returned.
        skip : int, default 0
            The number of rows to skip before returning (for pagination).
        **filters : key-value mapping
            Values you want to filter on. Keys must be part of self.facets.

        Returns
        -------
        sample : DataFrame
            A sample from the data.
        """
        raise NotImplementedError()

    def fastapi_serve(self, fast_api, uri):
        """Create FastAPI endpoints to serve the dataset.

        Parameters
        ----------
        fast_api : fastapi.applications.FastAPI
            A FastAPI application object. A new endpoint will be added in this application.
        uri : str
            The relative uri where the endpoint will be added.

        Returns
        -------
        Nothing : The endpoint is created as a side effect (inplace) in the `fast_api` application.
        """
        uri = '/' + uri.strip('/')
        import forge
        facet = forge.kwarg('facet', type=str)
        rows = forge.kwarg('rows', default=10, type=Optional[int])
        skip = forge.kwarg('skip', default=0, type=Optional[int])
        kwargs = [forge.kwarg(facet, default=None, type=Optional[str])
                  for facet in self.facets]

        @fast_api.get(uri + "/")
        def get_metadata():
            return as_json(self.metadata)

        @fast_api.get(uri + "/count")
        @forge.sign(*kwargs)
        def count(**kwargs):
            filters = {key: val for key, val in kwargs.items() if val is not None}
            count = self.count(**filters)
            return as_json({
                "count": int(count),
                "filters": filters,
                })

        @fast_api.get(uri + "/count-by/{facet}")
        @forge.sign(facet, rows, skip, *kwargs)
        def count_by(facet, rows=10, skip=0, **kwargs):
            filters = {key: val for key, val in kwargs.items() if val is not None}
            result = self.count_by(facet, rows=rows, skip=skip, **filters)
            return as_json({
                "facet": facet,
                # "count": len(result),  # TODO : add "nunique" feature in count_by schema
                "rows": len(result),
                "skip": skip,
                "filters": filters,
                "data": {str(key): int(val) for key, val in result.items()},
                })

        @fast_api.get(uri + "/sample")
        @forge.sign(rows, skip, *kwargs)
        def sample(rows=10, skip=0, **kwargs):
            filters = {key: val for key, val in kwargs.items() if val is not None}
            result = self.sample(rows=rows, skip=skip, **filters)
            count = self.count(**filters)
            return as_json({
                # "facet": facet,
                "count": count,
                "rows": len(result),
                "skip": skip,
                "filters": filters,
                "data": result.to_dict(orient='records'),
                })
