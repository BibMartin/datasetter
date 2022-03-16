# DataSetter

DataSetter helps you to create datasets with python, and serve them in a HTTP API.

A dataset is a product based on a homogeneous set of data. It is not only a table of data,
but also it's associated metadata :
- Name : A unique product name that identifies the product.
- Description : A short explaination of the product : what it contains, how it has been collected, what is can (or cannot) be used for...
- Columns : A description of the product 's components, with column names, types and description.
- Facets : The list of the columns that can be used to filter and/or aggregate data. In large datasets, it can ba a strict subset of the columns. 

For example, you can define a dataset based on a `pandas.DataFrame` object :

```python
>>> import pandas as pd
>>> from datasetter.pandas_dataset import PandasDataset
>>>
>>> dataframe = pd.DataFrame([
>>>     ['A', 'alpha', 1],
>>>     ['A', 'beta', 13],
>>>     ['A', 'gamma', 8],
>>>     ['B', 'alpha', 1],
>>>     ['B', 'beta', 31],
>>>     ['C', 'gamma', 9],
>>>     ['C', 'alpha', 2],
>>>     ['D', 'beta', 21],
>>>     ['D', 'gamma', 0],
>>>     ], columns=['letter', 'greek', 'number'])
>>>
>>> dataset = PandasDataset(
>>>     dataframe,
>>>     name="Random letters",
>>>     description="A simple dataset with letters, greek letters and integers.",
>>>     columns=[
>>>         {"name": "letter", "type": "string", "description": "A column with letters."},
>>>         {"name": "greek", "type": "string", "description": "A column with greek letters."},
>>>         {"name": "number", "type": "integer", "description": "A column with numbers."},
>>>         ],
>>>     facets=['letter', 'greek'])
```

Then, access it's methods in a standard way :

```python
>>> dataset.count()
9

>>> dataset.count(letter="A")
3

>>> dataset.sample(2, greek="gamma")
  letter  greek  number
2      A  gamma       8
5      C  gamma       9

>>> dataset.count_by('greek')
alpha    3
beta     3
gamma    3
Name: greek, dtype: int64

>>> dataset.metadata()
{'name': 'Random letters',
 'description': 'A simple dataset with letters, greek letters and integers.',
 'columns': [{'name': 'letter',
   'type': 'string',
   'description': 'A column with letters.'},
  {'name': 'greek',
   'type': 'string',
   'description': 'A column with greek letters.'},
  {'name': 'number',
   'type': 'integer',
   'description': 'A column with numbers.'}],
 'facets': ['letter', 'greek']}
```


## Create an API with `datasetter` and `fastapi`

Datasetter comes with a wrapper to simply create an API based on your datasets.
Based on the code above, just add :

```python
>>> from fastapi import FastAPI
>>> from datasetter.api import add_dataset

>>> app = FastAPI()
>>> add_dataset(app, 'random-letters', dataset)
```

Then your have a `fastAPI` application that you can run with `uvicorn` :

```bash
$ uvicorn main:app --host 0.0.0.0 --port 8000
```

or

```python
>>> import uvicorn
>>> uvicorn.run(
>>>     app,
>>>     host="0.0.0.0",
>>>     port=8000,
>>> )
```