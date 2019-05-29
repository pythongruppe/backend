import data_processing.sort as stats
import matplotlib.pyplot as plt
from data_collection.types import from_code
from io import StringIO
import urllib.parse


def create_property_type_cash_price_graph(df):
    data = stats.order_property_type_by_cash_price(df)

    def f(code):
        return str(from_code(code))

    types = list(map(f, data.keys()))
    return create_bar_graph(types, data.values(), bottom_pad=0.25)


def create_bar_graph(keys, values, bottom_pad=0.0):
    fig = plt.figure()
    ax = fig.gca()
    ax.bar(keys, values)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    fig.subplots_adjust(bottom=bottom_pad)
    return fig


def get_svg_xml(fig):
    img_data = StringIO()
    fig.savefig(img_data, format='svg')
    img_data.seek(0)  # rewind the data
    return img_data.getvalue()


def create_data_uri(svg_xml):
    svg_xml = svg_xml.replace('\r', '').replace('\n', '')
    encoded = urllib.parse.quote(svg_xml)  # url encode the svg xml string
    return f'data:image/svg+xml;utf8,{encoded}'
