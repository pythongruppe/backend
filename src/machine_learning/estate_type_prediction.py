from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

columns_keep = ["area_basement", "area_estate", "area_property", "rooms", "year", "zip"]


def create_pt_classifier(data):
    knn = KNeighborsClassifier()
    df = data
    df = df.fillna(0)
    y = df["property_type"]
    X = df[columns_keep]

    knn.fit(X,y)
    knn = KNeighborsClassifier(n_neighbors=3)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    knn.fit(X, y)
    acc = accuracy_score(y_test, knn.predict(X_test))

    def f(user_data):
        x = knn.predict(user_data)
        return x

    #decide optimal neighbor.
    mask = y != -1
    y_values = y.value_counts()
    for item in y_values.iteritems():
        if item[1] < 10 or item[1] > 1000:
            #change value in mask to fasle
            mask = mask & (y != item[0]) #bitwise operator is overloaded in pandas.

    y = y[mask]
    X = X[mask]
    k = _decide_best_neighbors(X, y, df['property_type'].unique())
    knn = KNeighborsClassifier(n_neighbors=k)
    return f, acc


def _decide_best_neighbors(X, y, neighbors):
    total_scores = []
    X_train, X_test, y_train, _ = train_test_split(X, y, test_size=0.33, random_state=42)
    for k in neighbors:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
        total_scores.append(scores.mean())
    MSE = [1 - x for x in total_scores] #Missclassification Error
    optimal_k = neighbors[MSE.index(min(MSE))]
    #_save_result_png(neighbors, MSE)
    return optimal_k


def _save_result_png(neighbors, MSE):
    plt.plot(neighbors, MSE)
    plt.xlabel("Neighbors amount")
    plt.ylabel("Missclassification Error by %")
    plt.show()
    #plt.savefig(neighbors, MSE)


#For testing if trainingset works.
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
#pred = knn.predict(X_test)
#print(accuracy_score(y_test, pred))


#for neighbors
#random_neighbors = list(range(1, 50))
