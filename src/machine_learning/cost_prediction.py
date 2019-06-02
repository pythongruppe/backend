from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def create_predictor(data, target, drop_columns):
    x = data.drop(columns=[target, *drop_columns], axis=1)
    y = data[target]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4)
    model = LinearRegression()
    model.fit(x_train, y_train)

    return model
