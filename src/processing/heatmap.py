import pandas as pd
import folium
from folium.plugins import HeatMap
import argparse
import os


def create_heat_map(df, key, save_file, query):
    df = df.dropna(subset=[key, 'longitude', 'latitude', 'zip'])
    if query is not None:
        df = df.query(query)

    max_value = df[key].max()
    f_map = folium.Map(location=[55.748433, 10.563504], zoom_start=7)  # center on denmark
    tuples = list(zip(df['latitude'], df['longitude'], df[key]))

    h_map = HeatMap(tuples, min_opacity=0.5, max_val=max_value, radius=3, blur=1)
    h_map.add_to(f_map)

    save_dir = os.path.dirname(save_file)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, 0o755)

    f_map.save(save_file)
    return f_map, h_map, df


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create and save to file a heat-map.")
    parser.add_argument('input', help='Path to input csv file')
    parser.add_argument('output', help='Path to output file')
    parser.add_argument('key',
                        help="The key in the dataset, that is plotted on the heat-map. Use multiple keys by seperating the keys with commas.")
    parser.add_argument('-f', '--filter', type=str, default=None, help='An optional pandas query to apply to the data.')

    args = vars(parser.parse_args())
    data = pd.read_csv(args['input'])
    keys = list(filter(lambda k: len(k) > 0, map(lambda k: k.strip(), args['key'].split(','))))

    for key in keys:
        output = args['output'].replace('*', key)
        _, _, data = create_heat_map(data, key, output, args['filter'])
        print(f'{len(data)} properties were used to create the heat-map with key {key}.')
        print(f'Saved to {output}')
