import requests
import bs4
import json


def find_results_page(page_number, page_size):
    url = f'https://www.boligsiden.dk/propertyresult/getdata?searchId=96a780b700d641929ec76b0e4b4c360f&pageNumber={page_number}&sortKey=12&sortDescending=false&displayTab=1&itemsPerPage={page_size}'
    response = requests.get(url)
    return json.loads(response.content)


def find_results():
    results = []
    page_number = 1
    page_size = 750
    while True:
        print(f'Fetching page number {page_number}')
        page_results = find_results_page(page_number, page_size)
        print(page_results)
        results.extend(page_results)
        page_number += 1
        if len(page_results) < page_size:
            return results


if __name__ == '__main__':
    print(len(find_results()))
