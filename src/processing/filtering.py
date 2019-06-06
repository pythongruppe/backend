from dataclasses import dataclass, asdict
from typing import List
from src.processing.nearby import search_by_coordinate_range, haversine


@dataclass
class LocationFilter:
    latitude: float = None
    longitude: float = None
    max_distance: float = None


@dataclass
class FilterParameters:
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

    zip_codes: List = None
    property_types: List = None

    nearby: LocationFilter = None


def filter_data_frame(df, parameters: FilterParameters):
    query = create_pandas_query(parameters)
    if len(query.strip()) < 1:
        return filter_by_location(df, parameters)
    else:
        return filter_by_location(df.query(query), parameters)


def filter_by_location(df, parameters: FilterParameters):
    print(parameters)
    if parameters.nearby is None:
        return df

    return search_by_coordinate_range(df, parameters.nearby.get("latitude"), parameters.nearby.get("longitude"),
                                      parameters.nearby.get("max_distance"), haversine)


def create_pandas_query(parameters: FilterParameters):
    parts = []
    parameter_dict = asdict(parameters)

    for name in ['area_basement', 'area_estate', 'area_property', 'cash_price', 'rooms', 'year']:
        parts.append(create_gtoe(name, f'{name}_min', parameter_dict))
        parts.append(create_ltoe(name, f'{name}_max', parameter_dict))

    parts.append(create_in('property_type', 'property_types', parameter_dict))
    parts.append(create_in('zip', 'zip_codes', parameter_dict))

    def function(x):
        return x is not None

    return ' and '.join(list(filter(function, parts)))


def create_gtoe(df_key, parameter_key, parameters):
    value = parameters.get(parameter_key, None)
    if value is not None:
        return f'{df_key} >= {value}'


def create_ltoe(df_key, parameter_key, parameters):
    value = parameters.get(parameter_key, None)
    if value is not None:
        return f'{df_key} <= {value}'


def create_in(df_key, parameter_key, parameters):
    value = parameters.get(parameter_key, None)
    if value is not None:
        comma_sep = ', '.join(list(map(str, value)))
        return f'{df_key} in [{comma_sep}]'
