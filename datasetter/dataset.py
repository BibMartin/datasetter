# Dataset : base class for datasetter
class FacetUnavailableError(Exception):
    """This class is used to raise exceptions due to unavailable facets."""
    pass


class Dataset(object):
    def __init__(self,
                 name=None,
                 description=None,
                 columns=None,
                 facets=None,
                 ):
        self.facets = facets
        self.name = name
        self.description = description
        self.columns = columns

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

    def metadata(self):
        return {
            "name": self.name,
            "description": self.description,
            "columns": self.columns,
            "facets": self.facets,
            }
