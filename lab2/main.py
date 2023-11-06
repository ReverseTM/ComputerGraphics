import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

vertices = np.array([
    [-2, -2, -2],
    [-1, -1, 1],
    [-2, 2, -2],
    [-1, 1, 1],
    [2, -2, -2],
    [1, -1, 1],
    [2, 2, -2],
    [1, 1, 1]
])

faces = np.array([
    [0, 1, 3, 2],
    [0, 4, 5, 1],
    [0, 2, 6, 4],
    [1, 5, 7, 3],
    [2, 3, 7, 6],
    [4, 6, 7, 5]
])

cube = [Poly3DCollection([vertices[face] for face in faces], alpha=1, facecolor='orange', edgecolor='k')]

ax.add_collection3d(cube[0])

ax.auto_scale_xyz([-2, 2], [-2, 2], [-2, 2])

plt.show()
