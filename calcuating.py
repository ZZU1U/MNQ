from sklearn.linear_model import LinearRegression


def train_model(X, Y):
    model = LinearRegression()
    model.fit(X, Y)

    return model
