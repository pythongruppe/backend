import matplotlib.pyplot as plt
import pandas as pd


def pos_masker(xs, ys):
    return xs > 0


def create_regresssion_graph(data, x_key, y_key, masker=pos_masker):
    fig = plt.figure()
    ax = fig.gca()
    xs = data[x_key]
    ys = data[y_key]
    mask = masker(xs, ys)

    xs = xs[mask]
    ys = ys[mask]

    ax.scatter(xs, ys, s=1)
    return fig, ax


# data = pd.read_csv('new_data.csv')
# lambda xs, ys: (xs >= 1500) & (ys < 10_000_000)
# fig, ax = create_regresssion_graph(data, 'zip', 'cash_price', lambda xs, ys: xs <= 30)
# fig.show()
# input()
