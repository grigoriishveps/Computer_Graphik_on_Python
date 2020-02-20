
from numpy import (linspace, logspace, zeros, ones, outer, meshgrid,
                   pi, sin, cos, sqrt, exp)
import numpy as np
from numpy.random import normal
import pylab
from mpl_toolkits.mplot3d import axes3d
from numpy import *
import matplotlib.pyplot as plt

cornerPoints = [
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 0]]

# тестовые координаты из учебника
print("use basic coords> y,n?")
#start = input()
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


def appendHvector(coords):
    b = np.array([[1]*len(coords)]).transpose()
    res = np.append(coords, b, axis=1)
    return res

def remove_last(x):
    #return x[..., :-1]
    return np.delete(x, 3, axis=1)

def rotationRelativeX(obj, angle):
    xOs = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle * (pi / 180)), np.sin(angle * (pi / 180)), 0],
        [0, -np.sin(angle * (pi / 180)), np.cos(angle * (pi / 180)), 0],
        [0, 0, 0, 1]])
    result = np.dot(obj, xOs)
    return result

def rotationRelativeY(obj, angle):
    yOs = np.array([
        [np.cos(angle * (pi / 180)), 0, -np.sin(angle * (pi / 180)), 0],
        [0, 1, 0, 0],
        [np.sin(angle * (pi / 180)), 0, np.cos(angle * (pi / 180)), 0],
        [0, 0, 0, 1]])
    result = np.dot(obj, yOs)
    return result


assotiationСoordSystem = remove_last(rotationRelativeX(appendHvector(assotiationСoordSystem), 0))
assotiationСoordSystem = remove_last(rotationRelativeY(appendHvector(assotiationСoordSystem), 0))
print(assotiationСoordSystem)
def f(u, w, coordMatrix):
    firstMatrix = np.array([1 - u, u])
    lastMatrix = np.array([[1 - w], [w]])
    res = []
    for i in range(3):
        middleMatrix = np.array([[coordMatrix[0][i], coordMatrix[1][i]],
                                 [coordMatrix[3][i], coordMatrix[2][i]]])
        result1 = np.dot(firstMatrix, middleMatrix)
        result2 = np.dot(result1, lastMatrix)
        res.append(result2[0])
    return res
# создаем 3д пространство
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

a = assotiationСoordSystem
print(a)
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
u = linspace(0, 1, N)

# декартово произведение всех возможных точек билинейной поверхности
buf = np.transpose([np.tile(u, len(u)), np.repeat(u, len(u))])

# цикл отрисовки каждой точки билинейной повехрности
for i in range(len(buf)):
    ax.scatter(f(buf[i][0], buf[i][1], assotiationСoordSystem)[0], f(buf[i][0], buf[i][1], assotiationСoordSystem)[1],
               f(buf[i][0], buf[i][1], assotiationСoordSystem)[2])

#print(f(0.5, 0.5, assotiationСoordSystem))
plt.show()
