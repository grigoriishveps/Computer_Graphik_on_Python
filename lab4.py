from copy import deepcopy
from tkinter import *
from typing import List
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

Info_x = []
Info_y = []


class Dot:
    def __init__(self, x_coord: float, y_coord: float):
        self.x = float(x_coord)
        self.y = float(y_coord)

    def __repr__(self):
        return f"[Point {self.x}, {self.y}]"


class Line:
    def __init__(self, start: Dot, end: Dot):
        self.start = start
        self.end = end


def convert_to_figure(list_of_coord: List[List[float]]):
    res = list()
    dot_array = [Dot(coord[0], coord[1]) for coord in list_of_coord]
    for k in range(len(dot_array) - 1):
        res.append(Line(dot_array[k], dot_array[k + 1]))
    res.append(Line(dot_array[-1], dot_array[0]))
    return res


def is_inside(point: Dot, line: Line):
    return (line.end.x - line.start.x) * (point.y - line.start.y) \
           > (line.end.y - line.start.y) * (point.x - line.start.x)


def find_point_of_intersection(first_line: Line, second_line: Line):
    num = (first_line.start.x * first_line.end.y - first_line.start.y * first_line.end.x) * (
            second_line.start.x - second_line.end.x) - (
                  first_line.start.x - first_line.end.x) * (
                  second_line.start.x * second_line.end.y - second_line.start.y * second_line.end.x)
    den = (first_line.start.x - first_line.end.x) * (second_line.start.y - second_line.end.y) - (
            first_line.start.y - first_line.end.y) * (
                  second_line.start.x - second_line.end.x)
    x = num / den
    # calc y part of dot
    num = (first_line.start.x * first_line.end.y - first_line.start.y * first_line.end.x) * (
            second_line.start.y - second_line.end.y) - \
          (first_line.start.y - first_line.end.y) * (
                  second_line.start.x * second_line.end.y - second_line.start.y * second_line.end.x)
    y = num / den
    return Dot(x, y)


def clip(dot_list: List[Dot], clipping_area: List[Line]):
    """
    Sutherland–Hodgman algorithm. Based on wikipedia pseudocode
    :param dot_list:
    :type dot_list:
    :param clipping_area:
    :type clipping_area:
    :return:
    :rtype:
    """
    result = dot_list
    for clipping_line in clipping_area:
        input_list = deepcopy(result)
        result.clear()
        for dot_index in range(len(input_list)):
            current_point = input_list[dot_index]
            prev_point = input_list[(dot_index + len(input_list) - 1) % len(input_list)]
            if is_inside(current_point, clipping_line):
                if not is_inside(prev_point, clipping_line):
                    inter_point = find_point_of_intersection(Line(prev_point, current_point), clipping_line)
                    result.append(inter_point)
                result.append(current_point)
            elif is_inside(prev_point, clipping_line):
                inter_point = find_point_of_intersection(Line(prev_point, current_point), clipping_line)
                result.append(inter_point)
    return result


def define_interface():
    list = root.grid_slaves()
    for l in list:
        l.destroy()

    x_label = []
    y_label = []
    x_entry = []
    y_entry = []

    k = int(subjectPolygon_tk.get())
    j = int(clipPolygon_tk.get())
    # Test data
    # k = 4
    # j = 9
    main_label1 = Label(text="Координаты фигуры:")
    main_label1.grid(row=0, column=0, columnspan=4)

    for i in range(k):
        Info_x.append(StringVar(0))
        Info_y.append(StringVar(0))

        x_label.append(Label(text="x:"))
        x_label[i].grid(row=i + 2, column=0, sticky="w")
        x_entry.append(Entry(textvariable=Info_x[i]))
        x_entry[i].grid(row=i + 2, column=1, padx=5, pady=5)
        y_label.append(Label(text="y:"))
        y_label[i].grid(row=i + 2, column=2, sticky="w")
        y_entry.append(Entry(textvariable=Info_y[i]))
        y_entry[i].grid(row=i + 2, column=3, padx=5, pady=5)

    main_label2 = Label(text="Координаты окна(окно должно быть выпуклое):")
    main_label2.grid(row=k + 3, column=0, columnspan=4)

    for i in range(j):
        Info_x.append(StringVar(0))
        Info_y.append(StringVar(0))

        x_label.append(Label(text="x:"))
        x_label[i + k].grid(row=k + 4 + i, column=0, sticky="w")
        x_entry.append(Entry(textvariable=Info_x[i + k]))
        x_entry[i + k].grid(row=k + 4 + i, column=1, padx=5, pady=5)
        y_label.append(Label(text="y:"))
        y_label[i + k].grid(row=k + 4 + i, column=2, sticky="w")
        y_entry.append(Entry(textvariable=Info_y[i + k]))
        y_entry[i + k].grid(row=k + 4 + i, column=3, padx=5, pady=5)

    message_button = Button(text="Draw", command=resolve)
    message_button.grid(row=k + j + 5, column=3, padx=5, pady=5, sticky="e")


def resolve():
    plt.clf()
    x = [float(data.get()) for data in Info_x]
    y = [float(data.get()) for data in Info_y]

    subjectPolygon = [[]]
    subjectPolygon.clear()

    k = int(subjectPolygon_tk.get())
    for i in range(k):
        subjectPolygon.append([x[i], y[i]])

    clipPolygon = [[]]
    clipPolygon.clear()
    j = int(clipPolygon_tk.get())
    for i in range(j):
        clipPolygon.append([x[i + k], y[i + k]])

    # Test data
    # subjectPolygon = [[50., 150.],
    #                   [200., 50.],
    #                   [350., 150.],
    #                   [350., 300.],
    #                   [250., 300.],
    #                   [200., 250.],
    #                   [150., 350.],
    #                   [100., 250.],
    #                   [50., 150.]]
    #
    # clipPolygon = [[100., 100.],
    #                [300., 100.],
    #                [300., 300.],
    #                [100., 300.], ]

    # subjectPolygon = [[115., 115.],
    #                   [115., 140.],
    #                   [140., 140.],
    #                   [140., 115.]]
    #
    # clipPolygon = [[100., 100.],
    #                [300., 100.],
    #                [300., 300.],
    #                [100., 300.]]

    figure_dot_array = [Dot(coord[0], coord[1]) for coord in subjectPolygon]
    # TODO -- convert_to_figure избыточен
    clip_area = convert_to_figure(clipPolygon)
    cv1 = clip(figure_dot_array, clip_area)
    print(cv1)
    clipPolygon.append([clipPolygon[0][0], clipPolygon[0][1]])
    subjectPolygon.append([subjectPolygon[0][0], subjectPolygon[0][1]])

    subjectPolygon = np.array(subjectPolygon)
    clipPolygon = np.array(clipPolygon)
    plt.plot(subjectPolygon[:, 0], subjectPolygon[:, 1], color="b", label="Исходный многоугольник")
    plt.plot(clipPolygon[:, 0], clipPolygon[:, 1], color="y", label="Выпуклый многоугольник отсечения")
    if len(cv1) != 0:
        result = [[dot.x, dot.y] for dot in cv1]
        result.append([result[0][0], result[0][1]])
        result = np.array(result)
        plt.plot(result[:, 0], result[:, 1], color="r", label="Обрезанная фигура")

    plt.minorticks_on()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-500, 500)
    plt.ylim(-500, 500)
    plt.legend(loc="best")
    plt.show()
    # canvas = FigureCanvasTkAgg(plt, master=root)
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    # canvas.draw()


if __name__ == '__main__':
    root = Tk()
    w = root.winfo_screenwidth() // 2 - 200
    h = root.winfo_screenheight() // 2 - 200
    root.title("Лабораторная №")
    root.geometry("400x400+{}+{}".format(w, h))
    root.resizable(False, False)

    main_label = Label(text="")
    main_label.grid(row=0, column=0, columnspan=4)

    subjectPolygon_tk = StringVar(0)
    clipPolygon_tk = StringVar(0)

    subjectPolygon_label = Label(text="Количество точек фигуры:")
    subjectPolygon_label.grid(row=1, column=0, sticky="w")
    subjectPolygon_entry = Entry(textvariable=subjectPolygon_tk)
    subjectPolygon_entry.grid(row=1, column=1, padx=5, pady=5)
    clipPolygon_label = Label(text="Количество точек окна:")
    clipPolygon_label.grid(row=2, column=0, sticky="w")
    clipPolygon_entry = Entry(textvariable=clipPolygon_tk)
    clipPolygon_entry.grid(row=2, column=1, padx=5, pady=5)
    message_button = Button(text="Next", command=define_interface)
    message_button.grid(row=4, column=3, padx=5, pady=5, sticky="e")

    root.mainloop()
