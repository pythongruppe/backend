from flask import Flask, request
from src.processing.filtering import FilterParameters, filter_data_frame
from rest_errors import json_error
from src.processing.numeric import find_min_mean_max
import traceback
from src.Memory import Memory
from flask import Response, jsonify, send_from_directory
from flask_cors import CORS
from src.collection.types import PropertyType
from src.logic.graphs import create_distribution_graphs, create_graph_cache
from src.logic.prediction import create_cost_predictor

app = Flask(__name__, static_url_path='/static', static_folder='public')
CORS(app)
memory = None
graph_cache = None
cost_predictor = None


def paginate(df, page_size, page_number):
    start = (page_number - 1) * page_size
    end = start + page_size
    return df.iloc[start: end]


@app.route('/graphs', methods=['GET'])
def graphs():
    return jsonify(create_distribution_graphs(graph_cache))

#
# @app.route('/static/<path:path>')
# def serve_static(path):
#     return send_from_directory('public', path)


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


@app.route('/predict', methods=['POST'])
def cost_prediction():
    sent = dict(request.json)
    return jsonify(cost_predictor(sent))


if __name__ == '__main__':
    print('Loading memory ...')
    memory = Memory('new_data.csv')
    graph_cache = create_graph_cache(memory.data)
    print(f'Loaded {len(memory.data)} records.')
    cost_predictor = create_cost_predictor(memory.data)

    app.run()
