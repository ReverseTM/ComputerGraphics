import matplotlib.pyplot as plt
import numpy as np


def f(x, y, a):
    return np.sign(x) * (np.abs(x)) ** (2 / 3) + np.sign(x) * (np.abs(y)) ** (2 / 3) - np.sign(x) * (np.abs(a)) ** (2 / 3)


def draw(a):
    x_min, x_max = -3, 3
    y_min, y_max = -3, 3

    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)

    plt.contour(X, Y, f(X, Y, a), levels=[0], colors='black')
    plt.axis('equal')

    plt.show()
