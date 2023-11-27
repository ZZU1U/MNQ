import numpy as np
from sklearn.linear_model import LinearRegression as linreg


class PredictionsModel:
    def train(self, X: np.array, Y: np.array) -> None:
        pass

    def predict(self, X: np.array) -> np.array:
        pass

    def info(self) -> str:
        pass


class LinearRegression(PredictionsModel):
    def __init__(self) -> None:
        self.name = 'f(x) = ax + b'
        self.model = linreg()

    def train(self, X: np.array, Y: np.array) -> None:
        self.model.fit(X, Y)

    def predict(self, X: np.array) -> np.array:
        return self.model.predict(X)

    def info(self):
        return f'a: {self.model.coef_[0][0]}, b: {self.model.intercept_[0]}'


class SimpleRegression(LinearRegression):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'f(x) = ax'
        self.model.fit_intercept = False

    def info(self):
        return f'a: {self.model.coef_[0][0]}'


class MeanValue(PredictionsModel):
    def __init__(self) -> None:
        self.mean_value = None
        self.name = 'f(x) = a'

    def train(self, X: np.array, Y: np.array):
        self.mean_value = np.mean(Y)

    def predict(self, X: np.array):
        return np.array([self.mean_value] * len(X))

    def info(self):
        return f'a: {self.mean_value}'