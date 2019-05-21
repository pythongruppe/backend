#%%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("properties.csv")

#splitting label and features
X = data.drop(columns=['cash_price', 'address', 'city', 'property_type'], axis=1)
y = data['cash_price']

# print(X_train.shape, y_train.shape)

# X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.4)

# # print(X_train.shape, y_train.shape)

# model = LinearRegression()
# model.fit(X_train,y_train)

# predictions = model.predict(X_test) 
# predictions

# print(type(X_train) == type(y_train))

sns.pairplot(data[:1000])
plt.show()