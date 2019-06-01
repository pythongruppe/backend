from sklearn.neighbors import KNeighborsClassifier

def create_estimator(data, user_data):
    knn = KNeighborsClassifier()
    data.drop(('address'), inplace=True, axis=1)
    data.drop(('city'), inplace=True, axis=1)
    y = data['property_type']
    data.drop(('property_type'), inplace=True, axis=1)
    knn.fit(data, y)
    pred = knn.predict(user_data)
    return pred

