import matplotlib as mpl
from matplotlib import pyplot as plt

def make_plot(X, Y, model):
    plt.scatter(X, Y, color='b')
    plt.plot(X, model.predict(X),color='r')

    plt.savefig('plot.png')
