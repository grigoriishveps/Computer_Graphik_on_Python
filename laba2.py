import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


# https://github.com/kawache/Python-B-spline-examples
# TODO: -- change coordinates online
# workable
# Разобраться с узловым вектором
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


if __name__ == '__main__':
    ctr = np.array([(50, 25), (59, 12), (50, 10), (57, 2),
                    (40, 4), (40, 14), (43, 17)])
    x = ctr[:, 0]
    y = ctr[:, 1]
    computer_and_draw_bspline(x, y)
