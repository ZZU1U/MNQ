import numpy as np
from sklearn.linear_model import LinearRegression as LinReg


class PredictionsModel:
    def train(self, x: np.array, y: np.array) -> None:
        pass

    def predict(self, x: np.array) -> np.array:
        pass

    def info(self) -> str:
        pass


class LinearRegression(PredictionsModel):
    def __init__(self) -> None:
        self.model = LinReg()

    def train(self, x: np.array, y: np.array) -> None:
        self.model.fit(x, y)

    def predict(self, x: np.array) -> np.array:
        return self.model.predict(x)

    def info(self):
        return f'a: {self.model.coef_[0][0]}, b: {self.model.intercept_[0]}'

    def name(self, x: str, y: str):
        return f'{y} = a{x} + b'


class SimpleRegression(LinearRegression):
    def __init__(self) -> None:
        super().__init__()
        self.model.fit_intercept = False

    def info(self):
        return f'a: {self.model.coef_[0][0]}'

    def name(self, x: str, y: str):
        return f'{y} = a{x}'


class MeanValue(PredictionsModel):
    def __init__(self) -> None:
        self.mean_value = None

    def train(self, x: np.array, y: np.array):
        self.mean_value = np.mean(y)

    def predict(self, x: np.array):
        return np.array([self.mean_value] * len(x))

    def info(self):
        return f'a: {self.mean_value}'

    def name(self, x: str, y: str):
        return f'{y} = a'
