import pandas as pd
import folium
from folium.plugins import HeatMap
import argparse
import os


def create_heat_map(df, save_file, query):
    df = df.dropna(subset=['longitude', 'latitude', 'zip'])
    if query is not None:
        df = df.query(query)

    f_map = folium.Map(location=[55.748433, 10.563504], zoom_start=7)  # center on denmark
    tuples = list(zip(df['latitude'], df['longitude']))

    h_map = HeatMap(tuples, min_opacity=0.3, radius=5, blur=3)
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
    parser.add_argument('-f', '--filter', type=str, default=None, help='An optional pandas query to apply to the data.')

    args = vars(parser.parse_args())
    data = pd.read_csv(args['input'])
    output = args['output']
    _, _, data = create_heat_map(data, output, args['filter'])
    print(f'{len(data)} properties were used to create the heat-map.')
    print(f'Saved to {output}')
