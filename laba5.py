from numpy import (linspace,logspace,zeros,ones,outer,meshgrid,
                   pi,sin,cos,sqrt,exp)
import pylab
import numpy as np
from numpy import *
import copy
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import pygame


print("use basic coords> y,n?")
#start = input()
start = 'y'
if(start=="y"):
    # x1, y1, z1 = 0,0,1
    # x2, y2, z2 = 1,1,1
    # x3, y3, z3 = 0,1,0
    # x4, y4, z4 = 1,0,0
    x1, y1, z1 = 0, 0, 1
    x2, y2, z2 = 0, 1, 1
    x3, y3, z3 = 1, 1, 1
    x4, y4, z4 = 1, 0, 1
else:
    print("Input bilinear coords")
    print("Input x1,y1,z1")
    x1,y1,z1 = float(input()),float(input()),float(input())
    print("Input x2,y2,z2")
    x2,y2,z2 = float(input()),float(input()),float(input())
    print("Input x3,y3,z3")
    x3,y3,z3 = float(input()),float(input()),float(input())
    print("Input x4,y4,z4")
    x4,y4,z4 = float(input()),float(input()),float(input())


assotiationСoordSystem = [
    [x1,y1,z1],
    [x2,y2,z2],
    [x3,y3,z3],
    [x4,y4,z4]
]



assotiationСoordSystem2 = copy.deepcopy(assotiationСoordSystem)

print(assotiationСoordSystem)
print(assotiationСoordSystem2)

for i in assotiationСoordSystem2:
    for j in range(len(i)):
        i[j]/=2


print(assotiationСoordSystem)
print(assotiationСoordSystem2)


def appendHvector(coords):
    for i in range(len(coords)):
        coords[i].append(1.0)
    return np.array(coords)

def deleteHvector(coords):
    for i in range(len(coords)):
        coords[i].append(1.0)
    return np.array(coords)

def remove_last(x):
    return x[...,:-1]

def rotationRelativeX(obj,angle):
        xOs = np.array([
            [1,0,0,0],
            [0,np.cos(angle*(pi/180)),np.sin(angle*(pi/180)),0],
            [0,-np.sin(angle*(pi/180)),np.cos(angle*(pi/180)),0],
            [0,0,0,1]
        ])
        result = np.dot(obj,xOs)
        return result


def rotationRelativeY(obj, angle):
    yOs = np.array([
        [np.cos(angle*(pi/180)), 0, -np.sin(angle*(pi/180)), 0],
        [0,1,0,0],
        [np.sin(angle * (pi / 180)),0, np.cos(angle * (pi / 180)), 0],
        [0, 0, 0, 1]
    ])
    result = np.dot(obj, yOs)
    return result


# assotiationСoordSystem = remove_last(rotationRelativeX(appendHvector(assotiationСoordSystem),10))
# assotiationСoordSystem = remove_last(rotationRelativeY(appendHvector(assotiationСoordSystem),90))
# assotiationСoordSystem2 = remove_last(rotationRelativeY(appendHvector(assotiationСoordSystem2),90))


singleSquare = [[0]*2]*4
assotiationСoord = [[0]*3]*4



def printMatrix ( matrix ):
   for i in range ( len(matrix) ):
      for j in range ( len(matrix[i]) ):
          print ( "{:4d}".format(matrix[i][j]), end = "" )
      print ()

printMatrix(singleSquare)
print(" n")
printMatrix(assotiationСoord)

def f(u,w, coordMatrix):
    firstMatrix = np.array([1-u, u])
    middleMatrix = np.array([
        [coordMatrix[0],coordMatrix[1]],
        [coordMatrix[3],coordMatrix[2]]])

    lastMatrix=np.array([
        [1-w],
        [w]
    ])

    result1 = np.dot(firstMatrix,middleMatrix)

    # промежуточные матрицы, для выполнения вычислений
    promResult=[[]]*2
    result2=[[]]*2

    # результат первого перемножения запиываем в промежуточную матрицу
    promResult[0] = result1[0]
    promResult[1] = result1[1]

    # результат второго перемножения запиываем в result 2
    result2[0] = np.dot(promResult[0],lastMatrix[0][0])
    result2[1] = np.dot(promResult[1],lastMatrix[1][0])

    # возвращаем координаты точки билинейной поверхности
    return result2[0]+result2[1]


# создаем 3д пространство
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X =[x3,x4,x1,x2,x3]
Y =[y3,y4,y1,y2,y3]
Z =[z3,z4,z1,z2,z3]

ax.set_xlabel('axis X')
ax.set_ylabel('axis Y')
ax.set_zlabel('axis Z')

# расставляем заданные опорные точки в сцене для 1 фигуры.
ax.scatter(assotiationСoordSystem[0][0], assotiationСoordSystem[0][1], assotiationСoordSystem[0][2])
ax.scatter(assotiationСoordSystem[1][0], assotiationСoordSystem[1][1], assotiationСoordSystem[1][2])
ax.scatter(assotiationСoordSystem[2][0], assotiationСoordSystem[2][1], assotiationСoordSystem[2][2])
ax.scatter(assotiationСoordSystem[3][0], assotiationСoordSystem[3][1], assotiationСoordSystem[3][2])
ax.plot(X, Y, Z)

# N - количество точек на поверхности
N =15
u = linspace(0,1,N)
w = linspace(0,1,N)

# декартово произведение всех возможных точек билинейной поверхности
buf = np.transpose([np.tile(u, len(u)), np.repeat(u, len(u))])

#цикл отрисовки каждой точки билинейной повехрности
for i in range(len(buf)):
        ax.scatter(f(buf[i][0],buf[i][1],assotiationСoordSystem)[0],
                   f(buf[i][0],buf[i][1],assotiationСoordSystem)[1],
                   f(buf[i][0],buf[i][1],assotiationСoordSystem)[2])

for i in range(len(buf)):
        ax.scatter(f(buf[i][0],buf[i][1],assotiationСoordSystem2)[0],
                   f(buf[i][0],buf[i][1],assotiationСoordSystem2)[1],
                   f(buf[i][0],buf[i][1],assotiationСoordSystem2)[2])


plt.show()

firstFigure = []
secondFigure = []

for i in range(len(buf)):
        bufferFirst = []
        bufferSec = []

        bufferFirst.append(f(buf[i][0],buf[i][1],assotiationСoordSystem)[0])
        bufferFirst.append(f(buf[i][0],buf[i][1],assotiationСoordSystem)[1])
        bufferFirst.append(f(buf[i][0],buf[i][1],assotiationСoordSystem)[2])

        bufferSec.append(f(buf[i][0], buf[i][1], assotiationСoordSystem2)[0])
        bufferSec.append(f(buf[i][0], buf[i][1], assotiationСoordSystem2)[1])
        bufferSec.append(f(buf[i][0], buf[i][1], assotiationСoordSystem2)[2])

        firstFigure.append(bufferFirst)
        secondFigure.append(bufferSec)

print(firstFigure)
print(secondFigure)

# реализуем Z-буфер
SIZE = 300

zbuff = [[-10000] * SIZE for i in range(SIZE)] # initialize z buffer to -inf

print(zbuff)
print(firstFigure.__len__())
print(len(firstFigure[0]))

for i in range(firstFigure.__len__()):
    for j in range(len(firstFigure[0])):
        if(firstFigure[i][2] > zbuff[i][j]):
            zbuff[i][j] = firstFigure[i][2]


for i in range(secondFigure.__len__()):
    for j in range(len(secondFigure[0])):
        if(secondFigure[i][2] > zbuff[i][j]):
            zbuff[i][j] = secondFigure[i][2]


# for i in range(150):
#     for j in range(150):
#         print(zbuff[i],end="\n")

pygame.init()

sc = pygame.display.set_mode((300, 200))

# здесь будут рисоваться фигуры

for i in firstFigure:
    for j in range(len(i)):
        i[j]*=150

for i in secondFigure:
    for j in range(len(i)):
        i[j]*=150


# попробуй хештаблицу
cache = {}

while 1:
    pygame.time.delay(1000)
    for i in pygame.event.get():
      if i.type == pygame.QUIT: exit()

    for i in range(firstFigure.__len__()):

        cache[firstFigure[i][0], firstFigure[i][1]] = firstFigure[i][2]
        if(firstFigure[i][2] > cache(firstFigure[i][0],firstFigure[i][1])):
            cache[firstFigure[i][0], firstFigure[i][1]] = firstFigure[i][2]
            pygame.draw.line(sc, (255,255,255), [firstFigure[i][0]+20, firstFigure[i][1]+20], [firstFigure[i][0]+20, firstFigure[i][1]+20], 3)
        elif(secondFigure[i][2] > cache(secondFigure[i][0],firstFigure[i][1])):
            cache[secondFigure[i][0], firstFigure[i][1]] =  secondFigure[i][2]
            pygame.draw.line(sc, (255, 0, 0), [secondFigure[i][0] + 20, secondFigure[i][1] + 20],[secondFigure[i][0] + 20, secondFigure[i][1] + 20], 3)

    pygame.display.update()
