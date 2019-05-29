import requests
import json
import pandas as pd
from common import create_arg_parser, write_or_append

columns_to_keep = [
    'basementSize', 'buildYear', 'city', 'latitude', 'longitude', 'lotSize',
    'price', 'propertyType', 'rooms', 'size', 'squaremeterPrice',
    'street', 'zipCode'
]

columns_to_rename = {
    'size': 'area_estate', 
    'lotSize': 'area_property',
    'basementSize': 'area_basement',
    'zipCode': 'zip',
    'price': 'cash_price',
    'buildYear': 'year',
    'squaremeterPrice': 'sq_meter_price',
    'exp': 'monthly_payment',
    'propertyType': 'property_type'
}


def get_results_for_page(page_number, page_size):
    url = f'https://api.boliga.dk/api/v2/search/results?page={page_number}&pageSize={page_size}'
    print(f'Fetching page {page_number} from {url}')
    response = requests.get(url)
    return json.loads(response.content)['results']


def get_all_results(max_results):
    results = []
    page_number = 1
    page_size = 500  # 500 is the max boliga allows
    while True:
        page_results = get_results_for_page(page_number, page_size)
        results.extend(page_results)
        page_number += 1
        if len(page_results) < page_size or len(results) >= max_results:
            df = pd.DataFrame(results[0:max_results])  # ensure that we only get max_results
            df = df[columns_to_keep]
            df.rename(columns=columns_to_rename, inplace=True)
            return df


if __name__ == '__main__':
    parser = create_arg_parser('Webscrape property data from boliga.dk')
    args = vars(parser.parse_args())
    save = args['save']
    found = get_all_results(args['max_results'])
    write_or_append(save, found, args['append'])
