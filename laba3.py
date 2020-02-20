from numpy import (linspace, pi)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# тестовые координаты из учебника
print("use basic coords y,n?")
# start = input()
start = 'y'
if (start == "y"):
    x1, y1, z1 = 0, 0, 1
    x2, y2, z2 = 1, 1, 1
    x3, y3, z3 = 0, 1, 0
    x4, y4, z4 = 1, 0, 0
else:
    print("Input bilinear coords")
    print("Input x1,y1,z1")
    x1, y1, z1 = float(input()), float(input()), float(input())
    print("Input x2,y2,z2")
    x2, y2, z2 = float(input()), float(input()), float(input())
    print("Input x3,y3,z3")
    x3, y3, z3 = float(input()), float(input()), float(input())
    print("Input x4,y4,z4")
    x4, y4, z4 = float(input()), float(input()), float(input())

assotiationСoordSystem = np.array([
    [x1, y1, z1],
    [x2, y2, z2],
    [x3, y3, z3],
    [x4, y4, z4]])


def append_hvector(coords):
    b = np.array([[1] * len(coords)]).transpose()
    return np.append(coords, b, axis=1)


def remove_last(x):
    # return x[..., :-1]
    return np.delete(x, 3, axis=1)


def rotation_relativeX(obj, angle):
    xOs = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle * (pi / 180)), np.sin(angle * (pi / 180)), 0],
        [0, -np.sin(angle * (pi / 180)), np.cos(angle * (pi / 180)), 0],
        [0, 0, 0, 1]])
    result = np.dot(obj, xOs)
    return result


def rotation_relativeY(obj, angle):
    yOs = np.array([
        [np.cos(angle * (pi / 180)), 0, -np.sin(angle * (pi / 180)), 0],
        [0, 1, 0, 0],
        [np.sin(angle * (pi / 180)), 0, np.cos(angle * (pi / 180)), 0],
        [0, 0, 0, 1]])
    result = np.dot(obj, yOs)
    return result


assotiationСoordSystem = remove_last(rotation_relativeX(append_hvector(assotiationСoordSystem), 0))
assotiationСoordSystem = remove_last(rotation_relativeY(append_hvector(assotiationСoordSystem), 0))


def f(u, w, coordMatrix):
    first_matrix = np.array([1 - u, u])
    last_matrix = np.array([[1 - w], [w]])
    res = []
    for t in range(3):
        middle_matrix = np.array([[coordMatrix[0][t], coordMatrix[1][t]],
                                  [coordMatrix[3][t], coordMatrix[2][t]]])
        result1 = np.dot(first_matrix, middle_matrix)
        result2 = np.dot(result1, last_matrix)
        res.append(result2[0])
    return res


# создаем 3д пространство
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = assotiationСoordSystem
'''X = [x3, x4, x1, x2, x3]
Y = [y3, y4, y1, y2, y3]
Z = [z3, z4, z1, z2, z3]'''
X = [a[2][0], a[3][0], a[0][0], a[1][0], a[2][0]]
Y = [a[2][1], a[3][1], a[0][1], a[1][1], a[2][1]]
Z = [a[2][2], a[3][2], a[0][2], a[1][2], a[2][2]]

ax.set_xlabel('axis X')
ax.set_ylabel('axis Y')
ax.set_zlabel('axis Z')

# расставляем заданные опорные точки в сцене.
for i in range(4):
    ax.scatter(assotiationСoordSystem[i][0], assotiationСoordSystem[i][1], assotiationСoordSystem[i][2])
ax.plot(X, Y, Z)

# N - количество точек на поверхности
N = 15
dots = linspace(0, 1, N)

# декартово произведение всех возможных точек билинейной поверхности
buf = np.transpose([np.tile(dots, len(dots)), np.repeat(dots, len(dots))])

# цикл отрисовки каждой точки билинейной повехрности
for i in range(len(buf)):
    xyz = f(buf[i][0], buf[i][1], assotiationСoordSystem)
    ax.scatter(xyz[0], xyz[1], xyz[2])

# print(f(0.5, 0.5, assotiationСoordSystem))
plt.show()
