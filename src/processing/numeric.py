from numpy import nanmean, nanmin, nanmax


def find_min_mean_max(data, columns):
    data = data[(data.T != 0).any()]
    return data[columns].agg([nanmin, nanmax, nanmean])


def find_min(data, columns):
    data = data[(data.T != 0).any()]
    return data[columns].agg(['min'])


def find_max(data, columns):
    data = data[(data.T != 0).any()]
    return data[columns].agg(['max'])


def find_mean(data, columns):
    data = data[(data.T != 0).any()]
    return data[columns].agg(['mean'])


