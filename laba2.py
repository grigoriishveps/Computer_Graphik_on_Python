import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

# workable
ctr = np.array([(50, 25), (59, 12), (50, 10), (57, 2),
                (40, 4), (40, 14), (43, 17)])
x = ctr[:, 0]
y = ctr[:, 1]

# uncomment both lines for a closed curve
# x=np.append(x,[x[0]])
# y=np.append(y,[y[0]])
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
l = len(x)
u3 = np.linspace(0, 1, (max(l * 2, 70)), endpoint=True)
plt.plot(x, y, 'k--', label='Control polygon', marker='o', markerfacecolor='red')
plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
plt.title('Cubic B-spline curve evaluation')
for k in range(1, 7):
    number_of_internal_knots = l - k + 1
    t = np.linspace(0, 1, number_of_internal_knots, endpoint=True)
    t = np.append([0] * k, t)
    t = np.append(t, [1] * k)
    tck = [t, [x, y], k]
    out = interpolate.splev(u3, tck)
    # plt.plot(x,y,'ro',label='Control points only')
    plt.plot(out[0], out[1], colors[k - 1], linewidth=2.0, label=f'B-spline curve {k} degree')
plt.legend(loc='best')
plt.show()


# /workable

def b_coefficients(x, k, i, t):
    if k == 0:
        return 1.0 if t[i] <= x < t[i + 1] else 0.0
    if t[i + k] == t[i]:
        c1 = 0.0
    else:
        c1 = (x - t[i]) / (t[i + k] - t[i]) * b_coefficients(x, k - 1, i, t)
    if t[i + k + 1] == t[i + 1]:
        c2 = 0.0
    else:
        c2 = (t[i + k + 1] - x) / (t[i + k + 1] - t[i + 1]) * b_coefficients(x, k - 1, i + 1, t)
    return c1 + c2

# np.array(si.splev(u, (kv, cv.T, degree))).T
# # cv – массив исходных контрольных точек
# # degree – степень кривых
# # u – диапозон кривых
# # kv – вектор узов
# # Оценка значения сглаживающего полинома и его производных:
# if isinstance(tck, BSpline):
#     if tck.c.ndim > 1:
#         mesg = ("Calling splev() with BSpline objects with c.ndim > 1 is "
#                "not recommended. Use BSpline.__call__(x) instead.")
#         warnings.warn(mesg, DeprecationWarning)
#     try:
#         extrapolate = {0: True, }[ext]
#     except KeyError:
#         raise ValueError("Extrapolation mode %s is not supported "
#                          "by BSpline." % ext)
#     return tck(x, der, extrapolate=extrapolate)
# else:
#     return _impl.splev(x, tck, der, ext)
#
# # Расчет интеграла B-сплайна между двумя заданными точками:
# if isinstance(tck, BSpline):
#         return tck.integrate(a, b, extrapolate=False)
#     else:
#         return _impl.splint(a, b, tck, full_output)
#
# # Нахождение корней кубического B-сплайна:
#         sh = tuple(range(c.ndim))
#         c = c.transpose(sh[1:] + (0,))
#         return _impl.sproot((t, c, k), mest)
#     else:
#         return _impl.sproot(tck, mest)
# # Расчет всех производных B-сплайна:
#         c[0][0]
#         parametric = True
#     except Exception:
#         parametric = False
#     if parametric:
#         return list(map(lambda c, x=x, t=t, k=k:
#                         spalde(x, [t, c, k]), c))
#
# # Нахождение двумерного представление поверхности:
# tx, ty = _surfit_cache['tx'], _surfit_cache['ty']
#     wrk = _surfit_cache['wrk']
#     u = nxest - kx - 1
#     v = nyest - ky - 1
#     km = max(kx, ky) + 1
#     ne = max(nxest, nyest)
#     bx, by = kx*v + ky + 1, ky*u + kx + 1
#     b1, b2 = bx, bx + v - ky
#     if bx > by:
#         b1, b2 = by, by + u - kx
#     msg = "Too many data points to interpolate"
#     lwrk1 = _intc_overflow(u*v*(2 + b1 + b2) +
#                            2*(u + v + km*(m + ne) + ne - kx - ky) + b2 + 1,
#                            msg=msg)
