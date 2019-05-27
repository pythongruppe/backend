import argparse


def create_arg_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('save', help='Path to output file')
    parser.add_argument('-a', '--append', action='store_true', default=False,
                        help='Whether or not to append the data to the output file.')
    parser.add_argument('-m', '--max_results', type=int, default=10_000_000, help='Maximum number of results')

    return parser
