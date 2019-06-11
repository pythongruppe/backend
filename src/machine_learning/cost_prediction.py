import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

columns_keep = ["area_basement", "area_estate", "area_property", "property_type", "rooms", "year", "zip"]


def _create_predictor(df, target, keep_columns):
    df = df.fillna(0)
    X = df[keep_columns]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0)

    model = LinearRegression()
    model.fit(X_train, y_train)
    # x = model.predict(X_test)

    def predict_input(user_data):
        user_data = user_data[columns_keep]
        prediction = model.predict(user_data)
        return pd.DataFrame(np.maximum(prediction, 0))

    return predict_input


def get_predictors(data):
    return _create_predictor(data, "cash_price", columns_keep), \
           _create_predictor(data, "monthly_payment", columns_keep), \
           _create_predictor(data, "down_payment", columns_keep)
