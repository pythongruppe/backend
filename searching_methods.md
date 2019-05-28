# Searching Methods

## Using `for`-loops and python `if`

```python
from dataclasses import dataclass, field
from data.types import PropertyType
from typing import List
import pandas as pd


# area_basement, area_estate, area_property, cash_price, property_type, rooms, year, zip

@dataclass(init=False)
class SearchParameters:
    area_basement_min: float = None
    area_basement_max: float = None

    area_estate_min: float = None
    area_estate_max: float = None

    area_property_min: float = None
    area_property_max: float = None

    cash_price_min: float = None
    cash_price_max: float = None

    rooms_min: float = None
    rooms_max: float = None

    year_min: float = None
    year_max: float = None

    zip_codes: List[float] = field(default_factory=list)
    property_types: List[PropertyType] = field(default_factory=list)


def search(df, parameters: SearchParameters):
    def f(row):
        return check_filter(row[1], parameters)

    mask = list(map(f, df.iterrows()))
    return df[mask]


def check_filter(row, parameters: SearchParameters):

    if parameters.area_basement_min is not None and parameters.area_basement_min > row['area_basement']:
        return False
    if parameters.area_basement_max is not None and parameters.area_basement_max < row['area_basement']:
        return False

    if parameters.area_estate_min is not None and parameters.area_estate_min > row['area_estate']:
        return False
    if parameters.area_estate_max is not None and parameters.area_estate_max < row['area_estate']:
        return False

    if parameters.area_property_min is not None and parameters.area_property_min > row['area_property']:
        return False
    if parameters.area_property_max is not None and parameters.area_property_max < row['area_property']:
        return False

    if parameters.cash_price_min is not None and parameters.cash_price_min > row['cash_price']:
        return False
    if parameters.cash_price_max is not None and parameters.cash_price_max < row['cash_price']:
        return False

    if parameters.rooms_min is not None and parameters.rooms_min > row['rooms']:
        return False
    if parameters.rooms_max is not None and parameters.rooms_max < row['rooms']:
        return False

    if parameters.year_min is not None and parameters.year_min > row['year']:
        return False
    if parameters.year_max is not None and parameters.year_max < row['year']:
        return False

    return True


if __name__ == '__main__':
    import time

    start = time.time()
    search_parameters = SearchParameters()
    search_parameters.cash_price_max = 5_000_000
    data = pd.read_csv('new_data.csv')
    print(len(data))
    results = search(data, search_parameters)
    print(len(results))
    end = time.time()
    print(end - start)
    print(f'max={results["cash_price"].max()}')

```
The results were
````
(base) C:\Users\Thomas\Documents\Datamatiker\4.semester\python\exam-backend>python src/searching.py
134461
124708
17.267749786376953
max=5000000
````

## Using numpy masks

From https://stackoverflow.com/a/30778300

`````python
from dataclasses import dataclass, field
from data.types import PropertyType
from typing import List
import pandas as pd
import numpy as np
import functools

# area_basement, area_estate, area_property, cash_price, property_type, rooms, year, zip

@dataclass(init=False)
class SearchParameters:
    area_basement_min: float = None
    area_basement_max: float = None

    area_estate_min: float = None
    area_estate_max: float = None

    area_property_min: float = None
    area_property_max: float = None

    cash_price_min: float = None
    cash_price_max: float = None

    rooms_min: float = None
    rooms_max: float = None

    year_min: float = None
    year_max: float = None

    zip_codes: List[float] = field(default_factory=list)
    property_types: List[PropertyType] = field(default_factory=list)


def search(df, parameters: SearchParameters):

    mask = create_mask(df, parameters)
    return df[mask]


def create_mask(rows, parameters: SearchParameters):

    conditions = []

    if parameters.area_basement_min is not None:
        conditions.append(rows['area_basement'] > parameters.area_basement_min)
    if parameters.area_basement_max is not None:
        conditions.append(rows['area_basement'] < parameters.area_basement_max)

    if parameters.area_estate_min is not None:
        conditions.append(rows['area_estate'] > parameters.area_estate_min)
    if parameters.area_estate_max is not None:
        conditions.append(rows['area_estate'] < parameters.area_estate_max)

    if parameters.area_property_min is not None:
        conditions.append(rows['area_property'] > parameters.area_property_min)
    if parameters.area_property_max is not None:
        conditions.append(rows['area_property'] < parameters.area_property_max)

    if parameters.cash_price_min is not None:
        conditions.append(rows['cash_price'] > parameters.cash_price_min)
    if parameters.cash_price_max is not None:
        conditions.append(rows['cash_price'] < parameters.cash_price_max)

    if parameters.rooms_min is not None:
        conditions.append(rows['rooms'] > parameters.rooms_min)
    if parameters.rooms_max is not None:
        conditions.append(rows['rooms'] < parameters.rooms_max)

    if parameters.year_min is not None:
        conditions.append(rows['year'] > parameters.year_min)
    if parameters.year_max is not None:
        conditions.append(rows['year'] < parameters.year_max)

    return functools.reduce(np.logical_and, conditions)


if __name__ == '__main__':
    import time

    start = time.time()
    search_parameters = SearchParameters()
    search_parameters.cash_price_max = 5_000_000
    data = pd.read_csv('new_data.csv')
    print(len(data))
    results = search(data, search_parameters)
    print(len(results))
    end = time.time()
    print(end - start)
    print(f'max={results["cash_price"].max()}')
`````
The results:
````
(base) C:\Users\Thomas\Documents\Datamatiker\4.semester\python\exam-backend>python src/searching.py
134461
124666
0.4987802505493164
max=4999999
````

## Using `DataFrame.query`

`````python
from dataclasses import dataclass, field
from data.types import PropertyType
from typing import List
import pandas as pd


# area_basement, area_estate, area_property, cash_price, property_type, rooms, year, zip

@dataclass(init=False)
class SearchParameters:
    area_basement_min: float = None
    area_basement_max: float = None

    area_estate_min: float = None
    area_estate_max: float = None

    area_property_min: float = None
    area_property_max: float = None

    cash_price_min: float = None
    cash_price_max: float = None

    rooms_min: float = None
    rooms_max: float = None

    year_min: float = None
    year_max: float = None

    zip_codes: List[float] = field(default_factory=list)
    property_types: List[PropertyType] = field(default_factory=list)


def search(df, parameters: SearchParameters):
    query = create_query(parameters)
    return df.query(query)


def create_query(parameters: SearchParameters):

    parts = []

    if parameters.area_basement_min is not None:
        parts.append(f'area_basement > {parameters.area_basement_min}')
    if parameters.area_basement_max is not None:
        parts.append(f'area_basement < {parameters.area_basement_max}')
        
    if parameters.area_estate_min is not None:
        parts.append(f'area_estate > {parameters.area_estate_min}')
    if parameters.area_estate_max is not None:
        parts.append(f'area_estate < {parameters.area_estate_max}')
        
    if parameters.area_property_min is not None:
        parts.append(f'area_property > {parameters.area_property_min}')
    if parameters.area_property_max is not None:
        parts.append(f'area_property < {parameters.area_property_max}')

    if parameters.cash_price_min is not None:
        parts.append(f'cash_price > {parameters.cash_price_min}')
    if parameters.cash_price_max is not None:
        parts.append(f'cash_price < {parameters.cash_price_max}')
        
    if parameters.rooms_min is not None:
        parts.append(f'rooms > {parameters.rooms_min}')
    if parameters.rooms_max is not None:
        parts.append(f'rooms < {parameters.rooms_max}')
        
    if parameters.year_min is not None:
        parts.append(f'year > {parameters.year_min}')
    if parameters.year_max is not None:
        parts.append(f'year < {parameters.year_max}')

    return ' and '.join(parts)

if __name__ == '__main__':
    import time

    start = time.time()
    search_parameters = SearchParameters()
    search_parameters.cash_price_max = 5_000_000
    data = pd.read_csv('new_data.csv')
    print(len(data))
    results = search(data, search_parameters)
    print(len(results))
    end = time.time()
    print(end - start)
    print(f'max={results["cash_price"].max()}')

`````

The results:

````
(base) C:\Users\Thomas\Documents\Datamatiker\4.semester\python\exam-backend>python src/searching.py
134461
124666
0.4589419364929199
max=4999999
````

## Scaling: `masks` vs `DataFrame.query`

Using more parameters:

````python
search_parameters = SearchParameters()
search_parameters.cash_price_max = 5_000_000
search_parameters.cash_price_min = 1_000_000
search_parameters.rooms_min = 4
search_parameters.area_property_min = 200
````

The results for numpy masks:
````
(base) C:\Users\Thomas\Documents\Datamatiker\4.semester\python\exam-backend>python src/searching.py
134461
40029
0.4519987106323242
max=4999999
````

The results for ``DataFrame.query``:

````
(base) C:\Users\Thomas\Documents\Datamatiker\4.semester\python\exam-backend>python src/searching.py
134461
40029
0.4669992923736572
max=4999999
````

## Conclusion

* Manual `for`-loops with python `if`-statements are too slow.
* The performance of numpy masks and ``DataFrame.query`` are the same.
* The performance of numpy masks and ``DataFrame.query`` does not suffer when the number of search parameters increase.