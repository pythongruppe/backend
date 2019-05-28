import statistics as stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from data.types import from_code
from io import StringIO
import urllib.parse

class GraphGenerator:

    def __init__(self, df):
        self.df = df

    def create_property_type_cash_price_graph(self):
        data = stats.order_property_type_by_cash_price(self.df)
        def f(code):
            return str(from_code(code))
        types = list(map(f, data.keys()))
        return self.create_bar_graph(types, data.values(), bottom_pad=0.25)

    def create_bar_graph(self, keys, values, bottom_pad=0.0):
        fig = plt.figure()
        ax = fig.gca()
        ax.bar(keys, values)
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)
        fig.subplots_adjust(bottom=bottom_pad)
        return fig

def get_xml(fig):
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    return imgdata.getvalue()

def create_data_uri(svg_xml):
    svg_xml = svg_xml.replace("\r","").replace("\n","")
    encoded = urllib.parse.quote(svg_xml)  # url encode the svg xml string
    return f'data:image/svg+xml;utf8,{encoded}'

if __name__ == '__main__':
    data = pd.read_csv('new_data.csv')
    gen = GraphGenerator(data)
    fig = gen.create_property_type_cash_price_graph()
    print(create_data_uri(get_xml(fig)))