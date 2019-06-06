from math import cos, asin, sqrt
import pandas as pd
import numpy as np
import time
import mpu

t0 = time.time()


def search_by_coordinate_range(data, lat, lon, max_distance, algo):
    distances = np.array([algo(lat, lon, row.latitude, row.longitude) for row in data.itertuples()])
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


# https://stackoverflow.com/a/15742266
def equirectangular(lat1, lon1, lat2, lon2):
    R = 6371  # radius of earth (km)
    x = abs(lon2 - lon1) * cos(0.5 * (lat2 + lat1))
    y = lat2 - lat1
    return R * sqrt(x * x + y * y)


def test(lat1, lon1, lat2, lon2):
    x = lat2 - lat1
    y = (lon2 - lon1) * cos((lat2 + lat1) * 0.00872664626)
    return 111.138 * sqrt(x * x + y * y)


def mpu_haversine(lat1, lon1, lat2, lon2):
    return mpu.haversine_distance((lat1, lon1), (lat2, lon2))


if __name__ == '__main__':
    data = pd.read_csv("new_data.csv")
    data = data[~(pd.isnull(data['latitude']) | pd.isnull(data['longitude']))]
    results = search_by_coordinate_range(data, 55.837491199999995, 12.4346368, 1, haversine)[['zip', 'street']]

    t1 = time.time()

    total = t1 - t0
    print(results)
    print(len(results))
    print(f'{total} seconds')
