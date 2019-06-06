from flask import Flask, request
from src.Memory import input_to_database
from src.processing.filtering import FilterParameters, filter_data_frame
from rest_errors import json_error
from src.processing.numeric import find_min_mean_max
import traceback
from src.Memory import Memory
from flask import Response, jsonify
from flask_cors import CORS
import json
import numpy as np
import pandas as pd
from src.machine_learning.estate_type_prediction import create_estimator
from src.collection.types import PropertyType

app = Flask(__name__)
CORS(app)
memory = None


def paginate(df, page_size, page_number):
    start = (page_number - 1) * page_size
    end = start + page_size
    return df.iloc[start: end]


@app.route('/filter', methods=['POST'])
def filter_stats():
    contents = request.get_json()
    page = max(request.args.get('page', default=1, type=int), 1)
    try:
        data = memory.data
        filter_parameters = FilterParameters(**contents.get('query'))
        results = filter_data_frame(data, filter_parameters)
        statistics = prepare(find_min_mean_max(results, ['area_estate', 'area_property', 'cash_price', 'rooms']))
        paginated = prepare(paginate(results, 50, page)).to_dict('records')
        response = {'statistics': statistics.to_dict(), 'count': len(results), 'results': paginated}
        return jsonify(response), 200
    except TypeError as e:
        traceback.print_exc()
        return json_error("Illegal filter parameters", 422, e)


@app.route('/property-types', methods=['GET'])
def get_property_types():
    types = [{'name': t.name, 'value': t.value} for t in PropertyType]
    return jsonify(types)


def prepare(df):
    return df.fillna('NaN')


@app.route('/estate', methods=['POST'])
def get_estate_prediction():
    data = request.data

    user_data = json.loads(data)
    user_data_df = pd.DataFrame([user_data])
    predictor = create_estimator(memory.data)
    prediction = predictor(user_data_df)
    print(prediction)
    return 'everything ok'


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
    print("loading memory")
    memory = Memory('new_data.csv')
    print(f'loaded {len(memory.data)} records.')
    app.run()

# check i can get data
# check i can read to file
# check i will not read to file if already exists
# create unit tests for this
# refactor methods in memory.py into smaller methods
