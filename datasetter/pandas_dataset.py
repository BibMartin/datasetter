# Create a dataset, based on a pandas DataFrame
from datasetter.dataset import Dataset, FacetUnavailableError
import pandas as pd


class PandasDataset(Dataset):
    def __init__(self, dataframe, facets, metadata=None):
        self.data = dataframe
        self.facets = facets
        self.metadata = metadata

    def _facet_filters(self, **filters):
        ind = pd.Series(True, index=self.data.index)
        for key, val in filters.items():
            if key not in self.facets:
                raise FacetUnavailableError(key)
            ind = ind & (self.data[key] == val)
        return ind

    def count(self, **filters):
        ind = self._facet_filters(**filters)
        return ind.sum()

    def sample(self, rows=10, skip=0, **filters):
        ind = self._facet_filters(**filters)
        return self.data[ind].head(rows+skip).tail(rows)

    def count_by(self, facet, rows=10, skip=0, **filters):
        if facet not in self.facets:
            raise FacetUnavailableError(facet)
        ind = self._facet_filters(**filters)
        s = self.data[facet][ind].value_counts()
        return s.head(rows+skip).tail(rows)
