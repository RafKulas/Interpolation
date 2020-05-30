import csv
import time
import numpy as np
import scipy.linalg as sp
from matplotlib import pyplot


def S_function(points):
    def calculate_params():
        n = len(points)

        A = np.zeros((4 * (n - 1), 4 * (n - 1)))
        b = np.zeros((4 * (n - 1), 1))

        # S_i(x_i) = f(x_i)
        for i in range(n - 1):
            x, y = points[i]
            row = np.zeros(4 * (n - 1))
            row[4 * i + 3] = 1
            A[4 * i + 3] = row
            b[4 * i + 3] = (float(y))

        # S_i(x_i+1) = f(x_i+1)
        for i in range(n - 1):
            x_i, y_i = points[i + 1]
            x_i_1, y_i_1 = points[i]
            h = float(x_i) - float(x_i_1)
            row = np.zeros(4 * (n - 1))
            row[4 * i] = h ** 3
            row[4 * i + 1] = h ** 2
            row[4 * i + 2] = h ** 1
            row[4 * i + 3] = 1
            A[4 * i + 2] = row
            b[4 * i + 2] = float(y_i)

        # S_i-1'(x_i) = S_i'(x_i)

        for i in range(n - 2):
            x_i, y_i = points[i + 1]
            x_i_1, y_i_1 = points[i]
            h = float(x_i) - float(x_i_1)
            row = np.zeros(4 * (n - 1))
            row[4 * i] = 3 * (h ** 2)
            row[4 * i + 1] = 2 * h
            row[4 * i + 2] = 1
            row[4 * (i + 1) + 2] = -1
            A[4 * i] = row
            b[4 * i] = float(0)

        # S_i-1''(x_i) = S_i''(x_i)

        for i in range(n - 2):
            x_i, y_i = points[i + 1]
            x_i_1, y_i_1 = points[i]
            h = float(x_i) - float(x_i_1)
            row = np.zeros(4 * (n - 1))
            row[4 * i] = 6 * h
            row[4 * i + 1] = 2
            row[4 * (i + 1) + 1] = -2
            A[4 * (i + 1) + 1] = row
            b[4 * (i + 1) + 1] = float(0)

        # S_0''(x_0) = 0 and S_n-1''(x_n-1) = 0

        # x_0
        row = np.zeros(4 * (n - 1))
        row[1] = 2
        A[1] = row
        b[1] = float(0)

        # x_n-1
        row = np.zeros(4 * (n - 1))
        x_i, y_i = points[-1]
        x_i_1, y_i_1 = points[-2]
        h = float(x_i) - float(x_i_1)
        row[1] = 2
        row[-4] = 6 * h
        A[-4] = row
        b[-4] = float(0)

        lu, piv = sp.lu_factor(A)
        x = sp.lu_solve((lu, piv), b)
        return x

    params = calculate_params()

    def f(x):
        param_array = []
        row = []
        for param in params:
            row.append(param)
            if len(row) == 4:
                param_array.append(row.copy())
                row.clear()
        for i in range(1, len(points)):
            xi, yi = points[i - 1]
            xj, yj = points[i]
            if float(xi) <= x <= float(xj):
                a, b, c, d = param_array[i - 1]
                h = x - float(xi)
                return a * (h ** 3) + b * (h ** 2) + c * h + d

        return np.nan

    return f


def interpolate_with_spline(file, amount_of_points):
    f = open(file, 'r')
    data = list(csv.reader(f))
    k = len(data) // amount_of_points
    data = data[1:]
    i_data = data[::k]

    given_x = []
    given_y = []
    for point in i_data:
        x, y = point
        given_x.append(float(x))
        given_y.append(float(y))

    fun_S = S_function(i_data)

    x_arr = []
    y_arr = []
    interpolated_y = []
    for point in data:
        x, y = point
        x_arr.append(float(x))
        y_arr.append(float(y))
        interpolated_y.append(fun_S(float(x)))

    shift = -1 * interpolated_y.count(np.nan)
    end = time.time()
    pyplot.plot(x_arr, y_arr, 'r.', label='Pełen zakres danych')
    pyplot.plot(given_x, given_y, 'g.', label='Ograniczone dane do interpolacji')
    pyplot.plot(x_arr[:shift], interpolated_y[:shift], color='blue', label='Wynik interpolacji')
    pyplot.legend()
    pyplot.ylabel('Wysokość[m]')
    pyplot.xlabel('Odległość[m]')
    pyplot.title('Interpolacją Splajnami, ' + str(len(i_data)) + ' punkty(ów)\n' + file)
    pyplot.grid()
    pyplot.show()
    return end
