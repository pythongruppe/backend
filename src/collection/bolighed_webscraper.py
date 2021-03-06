import requests
import json
import pandas as pd
import numpy as np
from common import create_arg_parser, write_or_append

columns_to_keep = [
    'address_text',
    'antalrum',
    'arealbolig',
    'arealgrund',
    'ejerudgift',
    'kontantpris',
    'postnummer',
    'postnummernavn',
    'property_type',
    'udbetaling',
    'sq_meter_price',
    'latitude',  # added by preprocess
    'longitude',  # added by preprocess
    'created'  # added by preprocess
]

columns_to_rename = {
    'address_text': 'street',
    'antalrum': 'rooms',
    'arealbolig': 'area_estate',
    'arealgrund': 'area_property',
    'ejerudgift': 'monthly_payment',
    'kontantpris': 'cash_price',
    'postnummer': 'zip',
    'postnummernavn': 'city',
    'udbetaling': 'down_payment',
}


def get_results_for_page(page_number, page_size):
    offset = (page_number - 1) * page_size
    url = f'https://bolighed.dk/api/external/market/propertyforsale/?limit={page_size}&offset={offset}&view=list&ordering=mtid'
    print(f'Fetching page {page_number} from {url}')
    response = requests.get(url)
    return json.loads(response.content)['results']


def get_all_results(max_results):
    results = []
    page_number = 1
    page_size = 1000
    while True:
        page_results = get_results_for_page(page_number, page_size)
        results.extend(page_results)
        page_number += 1
        if len(page_results) < page_size or len(results) >= max_results:
            df = pd.DataFrame(preprocess(results[0:max_results]))  # ensure that we only get max_results
            df = df[columns_to_keep]
            df.rename(columns=columns_to_rename, inplace=True)
            return df


def preprocess(results):
    for result in results:
        geometry = result.pop('geometry', None)
        if geometry is not None:
            result['longitude'] = geometry['coordinates'][0]
            result['latitude'] = geometry['coordinates'][1]

        prices = result['prices']
        prices_len = len(prices)
        if (prices is None or prices_len < 1):
            result['created'] = np.NaN
        else:
            result['created'] = prices[prices_len - 1]['dt']

        # ensure that the property types match the types defined in types.py
        result['property_type'] = convert_property_type(result['property_type'])

    return results


types_conversion_table = {
    1: 1,
    2: 9,
    3: 2,
    4: 3,
    5: 5,
    6: 11,
    7: 6,
    8: 8,
    9: 7,
}


def convert_property_type(code):
    return types_conversion_table.get(int(code), 10)  # default 10


if __name__ == '__main__':
    parser = create_arg_parser('Webscrape property data from bolighed.dk')
    args = vars(parser.parse_args())
    save = args['save']
    found = get_all_results(args['max_results'])
    write_or_append(save, found, args['append'])
