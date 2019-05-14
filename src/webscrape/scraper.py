import requests
import json
import pandas as pd
import numpy as np

columns_to_drop = [
    "andelsbolig",
    "billeder",
    "broker",
    "energy_mark",
    "geometry",
    "is_lot",
    "latest_price_change",
    "local_url",
    "mtid",
    "stid",
    "price_change",
    "price_development",
    "prices",
    "property_type",
    "url"
]

columns_to_rename = {
    "address_text": "address",
    "antalrum": "rooms",
    "arealbolig": "area_estate",
    "arealgrund": "area_property",
    "ejerudgift": "monthly_payment",
    "kontantpris": "cash_price",
    "postnummer": "zip",
    "postnummernavn": "city",
    "type_name": "property_type",
    "udbetaling": "down_payment"
}


def find_results_page(page_number, page_size):
    offset = (page_number - 1) * page_size
    url = f'https://bolighed.dk/api/external/market/propertyforsale/?limit={page_size}&offset={offset}&view=list&ordering=mtid'
    print(url)
    response = requests.get(url)
    return json.loads(response.content)['results']


def find_results():
    results = []
    page_number = 1
    page_size = 1000
    while True:
        print(f'Fetching page number {page_number}')
        page_results = find_results_page(page_number, page_size)
        results.extend(page_results)
        page_number += 1
        if len(page_results) < page_size:
            frame = pd.DataFrame(results)
            frame.drop(columns_to_drop, axis=1, inplace=True)
            frame.rename(columns=columns_to_rename, inplace=True)
            return frame


save_name = "properties.csv"
if __name__ == '__main__':
    frame = find_results()
    frame.to_csv(save_name, index=False)
    print(f'Saved to {save_name}')
