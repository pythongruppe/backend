from flask import Flask, request
from src.Memory import input_to_database
from src.data_processing.filtering import FilterParameters, filter_data_frame
import pandas as pd
from rest_errors import json_error
from src.data_processing.numeric import find_min_mean_max
import traceback

app = Flask(__name__)


@app.route('/filter', methods=['GET'])
def filter_stats():
    contents = request.get_json()
    data = pd.read_csv('new_data.csv')
    try:
        filter_parameters = FilterParameters(**contents.get('query'))
        results = filter_data_frame(data, filter_parameters)
        statistics = find_min_mean_max(data, ['area_estate', 'area_property', 'cash_price', 'rooms'])
        print(statistics)
        print(results[results['year'] == 0.0])
        return str(len(results))
    except TypeError as e:
        traceback.print_exc()
        return json_error("Illegal filter parameters", 422, e)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # assumed request.data is json with proper formatting / attributes NO checking atm.
        return input_to_database(request.data)
    return 'Hello World!'


# @app.route('/getAllIds', methods=['GET'])
# def show_ids():
# return house_ids()


if __name__ == '__main__':
    app.run()

# check i can get data
# check i can read to file
# check i will not read to file if already exists
# create unit tests for this
# refactor methods in memory.py into smaller methods
