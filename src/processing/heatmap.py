import pandas as pd
import folium
from folium.plugins import HeatMap
import argparse
import os


def create_heat_map(df, key, save_file, query):
    df = df.dropna(subset=[key, 'longitude', 'latitude', 'zip'])
    if query is not None:
        df = df.query(query)

    max_value = df['cash_price'].max()
    f_map = folium.Map(location=[55.748433, 10.563504], zoom_start=8)  # center on denmark
    h_map = HeatMap(
        list(zip(df['latitude'], df['longitude'], df[key])),
        min_opacity=0.5,
        max_val=max_value,
        radius=3, blur=1,
        max_zoom=1)

    f_map.add_child(h_map)

    save_dir = os.path.dirname(save_file)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, 0o755)

    f_map.save(save_file)
    return f_map, h_map, df


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create and save to file a heat-map.")
    parser.add_argument('input', help='Path to input csv file')
    parser.add_argument('output', help='Path to output file')
    parser.add_argument('key', help="The key in the dataset, that is plotted on the heat-map.")
    parser.add_argument('-f', '--filter', type=str, default=None, help='An optional pandas query to apply to the data.')

    args = vars(parser.parse_args())
    data = pd.read_csv(args['input'])
    _, _, data = create_heat_map(data, args['key'], args['output'], args['filter'])
    print(f'{len(data)} properties were used to create the heat-map.')
    print(f'Saved to {args["output"]}')
