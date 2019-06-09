import matplotlib.pyplot as plt
import numpy as np


def create_bar_distribution_graph(data, key, key_format=str):
    counts = data[key].value_counts()
    xs = np.array(counts.keys().tolist())
    ys = np.array(counts.tolist())
    mask = ys > (len(data) / 1000)  # ignore small data: count < 0.1% of total
    fig = plt.figure()
    ax = fig.gca()
    ax.bar(list(map(key_format, xs[mask])), ys[mask])
    return fig, ax


def create_cont_distribution_graph(data, key, ):
    counts = data[key].value_counts()
    xs = np.array(counts.keys().tolist())
    ys = np.array(counts.tolist())
    mask = xs >= 1500
    fig = plt.figure()
    ax = fig.gca()
    ax.scatter(xs[mask], ys[mask], s=6)
    return fig, ax
