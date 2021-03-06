import argparse
import os
import pandas as pd
import numpy as np


def create_arg_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('save', help='Path to output file')
    parser.add_argument('-a', '--append', action='store_true', default=False,
                        help='Whether or not to append the data to the output file.')
    parser.add_argument('-m', '--max_results', type=int, default=10_000_000, help='Maximum number of results')

    return parser


def write_or_append(save, df, append):
    if append:
        exists = os.path.isfile(save)
        current = pd.read_csv(save) if exists else pd.DataFrame()
        df['zip'] = df['zip'].astype('int')
        concat = pd.concat([current, df], ignore_index=False, sort=True)
        sanitize(concat).to_csv(save, index=False)
        if exists:
            print(f'Appended to {save}')
        else:
            print(f'Saved to {save}')
    else:
        sanitize(df).to_csv(save, index=False)
        print(f'Saved to {save}')


def sanitize(data):
    zero_to_nan = ['area_basement', 'area_estate', 'area_property', 'cash_price', 'down_payment', 'rooms', 'year']
    columns = data.columns.intersection(zero_to_nan)
    data[columns] = data[columns].replace(0.0, np.NaN)
    mask = data['cash_price'] >= 10_000 & ((data['area_property'] >= 16) | (data['area_estate'] >= 16))
    data = data[mask]  # ignore false data
    data = data.drop_duplicates(subset=['street', 'zip'], keep="last", inplace=False)

    return data
