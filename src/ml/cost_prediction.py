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
    cash_predictor = create_predictor(df, "cash_price", ('address', 'city', 'property_type'))
    monthly_payment_predictor = create_predictor(df, "monthly_payment", ('address', 'city', 'property_type'))
    down_payment_predictor = create_predictor(df, "down_payment", ('address', 'city', 'property_type'))

    mean = 0
    for row in df.rows:
        actual = row['cash_price']
        prediction = cash_predictor.predict(row)
        print(f'actual={actual}, prediction={prediction}, diff={abs(actual - prediction)}')
        mean += prediction

    print(f'mean={mean / len(df)}')