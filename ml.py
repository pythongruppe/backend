#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("new_data.csv")

def _create_predictor(df, target, keep_columns):
    df = df.fillna(0)
    X = df[keep_columns]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    model = LinearRegression()
    model.fit(X_train,y_train)
    x = model.predict(X_test)

    def predict_input(df):
        x = model.predict(df)
        return pd.DataFrame(np.maximum(x, 0))

    return predict_input


columns_keep = ["area_basement", "area_estate", "area_property", "property_type", "rooms", "year", "zip"]
cash_predictor = _create_predictor(data, "cash_price", columns_keep)
monthly_payment_predictor = _create_predictor(data, "monthly_payment", columns_keep)
down_payment_predictor = _create_predictor(data, "down_payment", columns_keep)

def get_predictors():
    return cash_predictor, monthly_payment_predictor, down_payment_predictor


# print(cash_predictor, monthly_payment_predictor, down_payment_predictor)

# print(X_train.shape, y_train.shape)

# plt.scatter(X_train, y_train, color = 'red')
# plt.plot(X_train, cash_predictor.model.prediction, color = 'blue')
# plt.title('Price vs Rooms (Training set)')
# plt.xlabel('Price')
# plt.ylabel('Rooms')
# plt.show()