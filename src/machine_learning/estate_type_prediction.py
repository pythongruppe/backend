from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

columns_keep = ["area_basement", "area_estate", "area_property", "rooms", "year", "zip"]


def create_pt_classifier(data):
    knn = KNeighborsClassifier()
    df = data
    df = df.fillna(0)
    y = df["property_type"]
    X = df[columns_keep]
    knn = KNeighborsClassifier(n_neighbors=3)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    knn.fit(X, y)
    acc = accuracy_score(y_test, knn.predict(X_test))

    def f(user_data):
        x = knn.predict(user_data)
        return x

    return f, acc
