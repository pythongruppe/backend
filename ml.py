#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("properties.csv")[1000:]

def create_predictor(df, target, drop_columns):
    X = data.drop(columns=[target, *drop_columns], axis=1)
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.4)

    model = LinearRegression()
    model.fit(X_train,y_train)

    print(model.predict(X_test))

    return model

cash_predictor = create_predictor(data, "cash_price", ('address', 'city', 'property_type'))
monthly_payment_predictor = create_predictor(data, "monthly_payment", ('address', 'city', 'property_type'))
down_payment_predictor = create_predictor(data, "down_payment", ('address', 'city', 'property_type'))

print(cash_predictor, monthly_payment_predictor, down_payment_predictor)

# print(X_train.shape, y_train.shape)

# plt.scatter(X_train, y_train, color = 'red')
# plt.plot(X_train, predictions, color = 'blue')
# plt.title('Price vs Rooms (Training set)')
# plt.xlabel('Price')
# plt.ylabel('Rooms')
# plt.show()