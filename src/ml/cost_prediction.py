import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def create_predictor(data, target, drop_columns):
    x = data.drop(columns=[target, *drop_columns], axis=1)
    y = data[target]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4)

    model = LinearRegression()
    model.fit(x_train, y_train)

    return model


if __name__ == '__main__':
    df = pd.read_csv("properties.csv")
    to_drop = ['address', 'city', 'property_type']
    cash_predictor = create_predictor(df, "cash_price", to_drop)
    df = df.drop(columns=[*to_drop], axis=1)
    
    mean = 0
    test = df.iloc[:100]
    predictions = cash_predictor.predict(test.drop('cash_price', axis=1))
    for i in range(100):
        actual = test.iloc[i]['cash_price']
        prediction = predictions[i]
        print(f'actual={actual}, prediction={prediction}, diff={abs(actual - prediction)}')
        mean += prediction

    print(f'mean={mean / 100}')