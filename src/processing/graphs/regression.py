import matplotlib.pyplot as plt


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
