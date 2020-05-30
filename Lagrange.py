import csv
from matplotlib import pyplot
import time

def fi_function(points):
    def fi(x):
        result = 0
        n = len(points)
        for i in range(n):
            x_i, y_i = points[i]
            base = 1
            for j in range(n):
                if i != j:
                    x_j, y_j = points[j]
                    base *= (float(x) - float(x_j)) / (float(x_i) - float(x_j))
            result += float(y_i) * base
        return result

    return fi


def lagrange(file, amount_of_points, cut=False):
    f = open(file, 'r')
    data = list(csv.reader(f))
    jump = len(data) // amount_of_points
    i_data = data[1::jump]  # i_data is data for interpolation, we take only every k-th element,
    # excluding first one which is title
    given_x = []
    given_y = []
    for point in i_data:
        x, y = point
        given_x.append(float(x))
        given_y.append(float(y))

    fun_fi = fi_function(i_data)
    x_arr = []
    y_arr = []
    interpolated_y = []
    for point in data[1:]:
        x, y = point
        x_arr.append(float(x))
        y_arr.append(float(y))
        interpolated_y.append(fun_fi(float(x)))

    end = time.time()
    if cut is True:
        n = len(x_arr)//3
        m = len(given_x)//3
        pyplot.plot(x_arr[n:2*n], y_arr[n:2*n], 'r.', label='Pełen zakres danych')
        pyplot.plot(given_x[m:2*m], given_y[m:2*m], 'g.', label='Ograniczone dane do interpolacji')
        pyplot.plot(x_arr[n:2*n], interpolated_y[n:2*n], color='blue', label='Wynik interpolacji')
    else:
        pyplot.yscale('symlog')
        pyplot.plot(x_arr, y_arr, 'r.', label='Pełen zakres danych')
        pyplot.plot(given_x, given_y, 'g.', label='Ograniczone dane do interpolacji')
        pyplot.plot(x_arr, interpolated_y, color='blue', label='Wynik interpolacji')
    pyplot.legend()
    pyplot.ylabel('Wysokość[m]')
    pyplot.xlabel('Odległość[m]')
    pyplot.title('Interpolacja Lagrange\'a, ' + str(len(i_data)) + ' punkty(ow)\nPlik: ' + file)
    pyplot.grid()
    pyplot.show()
    return end
