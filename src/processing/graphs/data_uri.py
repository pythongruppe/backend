from io import StringIO
import urllib.parse


def get_svg_xml(fig):
    img_data = StringIO()
    fig.savefig(img_data, format='svg')
    img_data.seek(0)  # rewind the data
    return img_data.getvalue()


def create_data_uri(svg_xml):
    svg_xml = svg_xml.replace('\r', '').replace('\n', '')
    encoded = urllib.parse.quote(svg_xml)  # url encode the svg xml string
    return f'data:image/svg+xml;utf8,{encoded}'


def fig_to_data_uri(fig):
    svg_xml = get_svg_xml(fig)
    return create_data_uri(svg_xml)
