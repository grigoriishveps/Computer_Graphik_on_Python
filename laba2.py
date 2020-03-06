import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class mywindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lelist = []
        self.initUI()

    def initUI(self):
        mainWidget = self
        mainbox = QVBoxLayout()
        mainWidget.setLayout(mainbox)
        ctr = [(50, 25), (59, 12), (50, 10), (57, 2), (40, 4), (40, 14), (43, 17)]
        for i in range(1, 8):
            le1 = QLineEdit()
            le2 = QLineEdit()

            le1.setText(str(ctr[i - 1][0]))
            le2.setText(str(ctr[i - 1][1]))
            self.lelist.append([le1, le2])
            box = QHBoxLayout()
            box.addWidget(QLabel("x" + str(i)))
            box.addWidget(le1)
            box.addWidget(QLabel("y" + str(i)))
            box.addWidget(le2)
            mainbox.addLayout(box)

        buttonDraw = QPushButton('Draw')
        buttonDraw.resize(buttonDraw.sizeHint())
        buttonDraw.clicked.connect(self.drawFun)

        boxButtons = QHBoxLayout()
        boxButtons.addStretch(1)
        boxButtons.addWidget(buttonDraw)
        mainbox.addStretch(1)
        mainbox.addLayout(boxButtons)
        mainWidget.setGeometry(300, 300, 300, 200)
        mainWidget.setWindowTitle('Menubar')
        mainWidget.show()

    def drawFun(self):
        def b_coefficients(t, k, i, x):
            """
            :param t: Параметр функции
            :type t:
            :param k: Степень
            :type k:
            :param i: Индекс
            :type i:
            :param x: значения узлового вектора
            :type x:
            :return:
            :rtype:
            """
            if k == 0:
                return 1.0 if x[i] <= t < x[i + 1] else 0.0
            if x[i + k] == x[i]:
                c1 = 0.0
            else:
                c1 = (t - x[i]) / (x[i + k] - x[i]) * b_coefficients(t, k - 1, i, x)
            if x[i + k + 1] == x[i + 1]:
                c2 = 0.0
            else:
                c2 = (x[i + k + 1] - t) / (x[i + k + 1] - x[i + 1]) * b_coefficients(t, k - 1, i + 1, x)
            return c1 + c2

        def bspline(t, x, c, k):
            n = len(x) - k - 1
            assert (n >= k + 1) and (len(c) >= n)
            return sum(c[i] * b_coefficients(t, k, i, x) for i in range(n))

        def computer_and_draw_bspline(x, y):
            plt.close()
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
            length = len(x)
            u3 = np.linspace(0, 1, 70, endpoint=False)
            plt.plot(x, y, 'k--', label='Control polygon', marker='o', markerfacecolor='red')
            plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
            plt.title('Cubic B-spline curve evaluation')
            for k in range(1, 7):
                number_of_internal_knots = length - k + 1
                knot_vector = np.linspace(0, 1, number_of_internal_knots, endpoint=True)
                knot_vector = np.append([0] * k, knot_vector)
                knot_vector = np.append(knot_vector, [1] * k)
                plt.plot([bspline(z, knot_vector, x.tolist(), k) for z in u3],
                         [bspline(z, knot_vector, y.tolist(), k) for z in u3],
                         colors[k - 1], lw=2, label=f'B-spline curve {k} degree')
            plt.legend(loc='upper right')
            plt.show()

        ctr = np.array(self.lelist)
        x = ctr[:, 0]
        y = ctr[:, 1]

        x = list(map(lambda x: int(x.text()), x))
        x = np.array(x)
        y = list(map(lambda x: int(x.text()), y))
        y = np.array(y)
        print(x, y)
        computer_and_draw_bspline(x, y)


# https://github.com/kawache/Python-B-spline-examples

app = QApplication(sys.argv)
ms = mywindow()
sys.exit(app.exec_())
