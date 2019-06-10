from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

data = pd.read_csv("new_data.csv")
columns_keep = ["area_basement", "area_estate", "area_property", "rooms", "year", "zip"]

def create_estimator(data):
    knn = KNeighborsClassifier()
    df = data
    df = df.fillna(0)
    y = df["property_type"]
    X = df[columns_keep]
    knn = KNeighborsClassifier(n_neighbors=3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    knn.fit(X,y)
    #pred = knn.predict(X_test)
    #print(accuracy_score(y_test, pred))

    def f(userdata):
        x = knn.predict(userdata)
        return x
    return f

#property_predictor = _create_estimator(data)


def _decide_best_neighbors():
    return None
#data.fillna(data.mean(), inplace=True)
