import requests
import json
import pandas as pd
import folium
import argparse
import os
import numpy as np


def download_zip_bounds():
    response = requests.get("https://raw.githubusercontent.com/ok-dk/dagi/master/geojson/postnumre.geojson")
    with open("zip_bounds.json", "w") as f:
        f.write(response.text)


def create_choropleth_map(df, zip_bounds, key, save_file, query, min_value, max_value, unit, no_bins, spacing):
    df = df.dropna(subset=[key, 'zip'])
    if query is not None:
        df = df.query(query)

    f_map = folium.Map(location=[55.748433, 10.563504], zoom_start=7)  # center on denmark

    features = zip_bounds['features']
    for f in features:
        try:
            f['properties']['POSTNR_TXT'] = int(f['properties']['POSTNR_TXT'])
        except:
            pass

    means = df[['zip', key]].groupby('zip').mean()
    means['zip'] = means.index

    if min_value is not None:
        means = means[means[key] >= min_value]

    if max_value is not None:
        means = means[means[key] <= max_value]

    means[key] = means[means[key] > 0]
    means[key] = means[key] / unit
    minimum = max(means[key].min(), means[key].min() - (1 / unit))
    maximum = means[key].max() + (1 / unit)

    if spacing == 'log':
        bins = np.geomspace(minimum, maximum, num=no_bins + 1)
    else:
        bins = np.linspace(minimum, maximum, num=no_bins + 1)

    c_map = folium.Choropleth(
        geo_data=zip_bounds,
        data=means,
        fill_color='YlOrRd',
        columns=['zip', key],
        key_on='feature.properties.POSTNR_TXT',
        bins=bins
    )

    c_map.add_to(f_map)

    save_dir = os.path.dirname(save_file)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, 0o755)

    f_map.save(save_file)
    return f_map, c_map, df


def get_zip_bounds(feature_collection):
    fs = feature_collection['features']
    result = dict()
    for fea in fs:
        result[int(fea['properties']['nr'])] = fea['geometry']

    return result


# sq_meter_price,cash_price,area_basement,area_estate,area_property,rooms,year

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create and save to file a choropleth.")
    parser.add_argument('input', help='Path to input csv file')
    parser.add_argument('output', help='Path to output file')
    parser.add_argument('key',
                        help="The key in the dataset, that is plotted on the heat-map. Use multiple keys by seperating the keys with commas.")
    parser.add_argument('-f', '--filter', type=str, default=None, help='An optional pandas query to apply to the data.')
    parser.add_argument('--min', type=int, default=None, help='The lower bound for the value.')
    parser.add_argument('--max', type=int, default=None, help='The upper bound for the value.')
    parser.add_argument('-u', '--unit', type=int, default=1,
                        help='When given, all data points are first divided by the provided factor.')
    parser.add_argument('-b', '--bins', type=int, default=6, help='The number of bins to create for the data.')
    parser.add_argument('-s', '--spacing', type=str, default='lin', help='The bind spacing to use lin|log')

    args = vars(parser.parse_args())
    data = pd.read_csv(args['input'])
    keys = list(filter(lambda k: len(k) > 0, map(lambda k: k.strip(), args['key'].split(','))))

    with open('zip_bounds.json') as f:
        features = json.loads(f.read())
        for key in keys:
            output = args['output'].replace('*', key)
            _, _, data = create_choropleth_map(data, features, key, output, args['filter'],
                                               args['min'],
                                               args['max'],
                                               args['unit'],
                                               args['bins'], args['spacing'])
            print(f'{len(data)} properties were used to create the choropleth with key {key}.')
            print(f'Saved to {output}')
