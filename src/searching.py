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
    print(query)
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
