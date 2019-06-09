from flask import Flask, request
from src.Memory import input_to_database
from src.processing.filtering import FilterParameters, filter_data_frame
from rest_errors import json_error
from src.processing.numeric import find_min_mean_max
import traceback
from src.Memory import Memory
from flask import Response, jsonify
from flask_cors import CORS
from src.collection.types import PropertyType
from ml import get_predictors
import pandas as pd
from src.logic.graphs import create_distribution_graphs, create_graph_cache

app = Flask(__name__)
CORS(app)
memory = None
graphCache = None


def paginate(df, page_size, page_number):
    start = (page_number - 1) * page_size
    end = start + page_size
    return df.iloc[start: end]


@app.route('/graphs', methods=['GET'])
def graphs():
    return jsonify(create_distribution_graphs(graphCache))


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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # assumed request.data is json with proper formatting / attributes NO checking atm.
        return input_to_database(request.data)
    return 'Hello World!'


cash_predictor, monthly_payment_predictor, down_payment_predictor = get_predictors()


@app.route('/predict', methods=['POST'])
def ml():
    content = request.json
    d = dict(content)
    df = pd.DataFrame.from_dict({key: [value] for key, value in d.items()})
    cash_predition = cash_predictor(df)
    monthly_payment_prediction = monthly_payment_predictor(df)
    down_payment_prediction = down_payment_predictor(df)
    d = {'cash_prediction': cash_predition.iloc[0][0],
         'monthly_payment': monthly_payment_prediction.iloc[0][0],
         'down_payment': down_payment_prediction.iloc[0][0]
         }
    return jsonify(d)


if __name__ == '__main__':
    print("loading memory")
    memory = Memory('new_data.csv')
    graphCache = create_graph_cache(memory.data)
    print(f'loaded {len(memory.data)} records.')

    app.run()

# check i can get data
# check i can read to file
# check i will not read to file if already exists
# create unit tests for this
# refactor methods in memory.py into smaller methods
