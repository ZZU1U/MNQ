import numpy as np
from matplotlib import pyplot as plt
from calculating import *

def make_plot(X: np.array, Y: np.array, model: LinearRegression | SimpleRegression | MeanValue,\
              X_label: None | str = None, Y_label: None | str = None, filename: str = 'plot.png'):
    # First cleaning our last plot
    plt.cla()
    plt.clf()

    # Styling and plotting
    plt.style.use('Solarize_Light2')

    plt.scatter(X, Y, color='b')
    plt.plot(X, model.predict(X), color='r', )

    if X_label is not None:
        plt.xlabel(X_label)

    if Y_label is not None:
        plt.ylabel(Y_label)

    plt.savefig(filename)
