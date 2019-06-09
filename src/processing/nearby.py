from math import cos, asin, sqrt
import numpy as np


def search_by_coordinate_range(data, lat, lon, max_distance, algorithm):
    distances = np.array([algorithm(lat, lon, row.latitude, row.longitude) for row in data.itertuples()])
    return data.iloc[distances < max_distance]


# https://stackoverflow.com/a/21623206
def haversine(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


# https://blog.mapbox.com/fast-geodesic-approximations-with-cheap-ruler-106f229ad016
def pythagorean(lat1, lon1, lat2, lon2):
    y = 12430 * (abs(lat1 - lat2) / 180)
    x = 24901 * (abs(lon1 - lon2) / 360) * cos((lat1 + lat2) / 2)
    return sqrt(x ** 2 + y ** 2)
