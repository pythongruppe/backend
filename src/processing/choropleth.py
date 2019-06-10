import requests
import json
import pandas as pd
import folium
import argparse
import os
import numpy as np


def download_zip_bounds():
    response = requests.get("http://dawa.aws.dk/postnumre?format=geojson")
    with open("zip_bounds.json", "w") as f:
        f.write(response.text)


def create_choropleth_map(df, zip_bounds, key, save_file, query):
    df = df.dropna(subset=[key, 'zip'])
    if query is not None:
        df = df.query(query)

    f_map = folium.Map(location=[55.748433, 10.563504], zoom_start=7)  # center on denmark

    features = zip_bounds['features']
    for f in features:
        f['properties']['nr'] = int(f['properties']['nr'])

    means = df[['zip', key]].groupby('zip').mean()
    means['zip'] = means.index

    means = means[means[key] < 10_000_000]
    bins = np.geomspace(means[key].min() - 1, means[key].max() + 1, num=9)

    c_map = folium.Choropleth(
        geo_data=zip_bounds,
        data=means,
        fill_color='YlOrRd',
        columns=['zip', key],
        key_on='feature.properties.nr',
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create and save to file a choropleth.")
    parser.add_argument('input', help='Path to input csv file')
    parser.add_argument('output', help='Path to output file')
    parser.add_argument('key',
                        help="The key in the dataset, that is plotted on the heat-map. Use multiple keys by seperating the keys with commas.")
    parser.add_argument('-f', '--filter', type=str, default=None, help='An optional pandas query to apply to the data.')

    args = vars(parser.parse_args())
    data = pd.read_csv(args['input'])
    keys = list(filter(lambda k: len(k) > 0, map(lambda k: k.strip(), args['key'].split(','))))

    with open('zip_bounds.json') as f:
        features = json.loads(f.read())
        for key in keys:
            output = args['output'].replace('*', key)
            _, _, data = create_choropleth_map(data, features, key, output, args['filter'])
            print(f'{len(data)} properties were used to create the choropleth with key {key}.')
            print(f'Saved to {output}')
