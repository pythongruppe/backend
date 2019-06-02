from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def create_estimator(data):
    knn = KNeighborsClassifier()
    print(data)
    y = data['property_type']
    data.drop(columns=['street', 'city', 'property_type', 'latitude', 'longitude',\
    'created', 'area_basement', 'area_estate', 'area_estate'], axis=1, inplace=True)
    data.fillna(data.mean(), inplace=True)
    knn.fit(data, y)
    def f(userdata):
        return knn.predict(userdata)
    return f

