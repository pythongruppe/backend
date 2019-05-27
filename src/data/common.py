import argparse
import os
import pandas as pd


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
        pd.concat([current, df], ignore_index=True, sort=True).to_csv(save, index=False)
        if exists:
            print(f'Appended to {save}')
        else:
            print(f'Saved to {save}')
    else:
        df.to_csv(save, index=False)
        print(f'Saved to {save}')