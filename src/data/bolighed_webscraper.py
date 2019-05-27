import requests
import json
import pandas as pd
import os
from common import create_arg_parser

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
    'longitude'  # added by preprocess
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
    'udbetaling': 'down_payment'
}


def get_results_for_page(page_number, page_size):
    offset = (page_number - 1) * page_size
    url = f'https://bolighed.dk/api/external/market/propertyforsale/?limit={page_size}&offset={offset}&view=list&ordering=mtid'
    response = requests.get(url)
    return json.loads(response.content)['results']


def get_all_results(max_results):
    results = []
    page_number = 1
    page_size = 1000
    while True:
        print(f'Fetching page number {page_number}')
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

    return results


if __name__ == '__main__':
    parser = create_arg_parser('Webscrape property data from bolighed.dk')
    args = vars(parser.parse_args())
    save = args['save']
    found = get_all_results(args['max_results'])

    if args['append']:
        exists = os.path.isfile(save)
        current = pd.read_csv(save) if exists else pd.DataFrame()
        pd.concat([current, found], ignore_index=True, sort=True).to_csv(save, index=False)
        if exists:
            print(f'Merged with {save}')
        else:
            print(f'Appended to {save}')
    else:
        found.to_csv(save, index=False)
        print(f'Saved to {save}')
