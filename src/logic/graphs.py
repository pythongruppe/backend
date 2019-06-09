from src.processing.graphs.cache import GraphCache
from src.processing.graphs.data_uri import fig_to_data_uri
from src.processing.graphs.distribution import create_cont_distribution_graph, create_bar_distribution_graph
from src.collection.types import PropertyType


def create_graph_object(name, src):
    return {
        'name': name,
        'src': src
    }


def rotate_ticks(fig, ax, bottom_pad=0.0):
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    fig.subplots_adjust(bottom=bottom_pad)


def create_graph_cache(data):
    graph_cache = GraphCache(data)
    graph_cache.register('rooms', rooms)
    graph_cache.register('property_types', property_types)
    graph_cache.register('year', years)
    return graph_cache


def rooms(data):
    graph, ax = create_bar_distribution_graph(data, 'rooms')
    return fig_to_data_uri(graph)


def property_types(data):
    graph, ax = create_bar_distribution_graph(data, 'property_type', lambda x: PropertyType(x).name)
    rotate_ticks(graph, ax, bottom_pad=0.25)
    return fig_to_data_uri(graph)


def years(data):
    graph, ax = create_cont_distribution_graph(data, 'year')
    return fig_to_data_uri(graph)


def create_distribution_graphs(graph_cache):
    return [
        create_graph_object('Rooms Distribution', graph_cache.get('rooms')),
        create_graph_object('Year Distribution', graph_cache.get('year')),
        create_graph_object('Property Type Distribution', graph_cache.get('property_types'))]
