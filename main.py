import argparse
import os
import csv
import Lagrange
import Spline_I
from matplotlib import pyplot


def drawAlldata():
    for csvf in os.listdir('./paths'):
        if csvf != ".DS_Store":  # Problem while running on MacOS
            f = open('./paths/' + csvf, 'r')
            data = list(csv.reader(f))
            xs = []
            ys = []
            for point in data[1:]:
                x, y = point
                xs.append(float(x))
                ys.append(float(y))
            pyplot.plot(xs, ys, 'r.', label='Pełen zakres danych')
            pyplot.legend()
            pyplot.ylabel('Wysokość[m]')
            pyplot.xlabel('Odległość[m]')
            pyplot.title('Wizualizacja wszystkich punktówd\nPlik: ' + csvf)
            pyplot.grid()
            pyplot.show()


def strToBool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return True  # C/Cpp like parsing bool


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type",
                        help="L for Lagrange's interpolation or S for Spline method, both runned if none is selected")
    parser.add_argument("-p", "--points",
                        help="By rounding how many points you want to use for interpolation, 100 by default",
                        type=int)
    parser.add_argument("-f", "--file",
                        help="Path to file, ./path/ is set by default")
    parser.add_argument("-c", "--cut",
                        help="Can be used to cut of first and last 1/3 of data for Lagrange's interpolation, false by "
                             "default.",
                        type=strToBool)
    args, leftovers = parser.parse_known_args()

    points = 100
    if args.points is not None:
        points = args.points

    cut = False
    if args.cut is not None:
        cut = args.cut

    if args.type is None and args.file is None:
        if args.type is None:
            for file in os.listdir('./paths'):
                if file != ".DS_Store":  # Problem while running on MacOS
                    Lagrange.lagrange('./paths/' + file, points, cut=cut)
                    Spline_I.interpolate_with_spline('./paths/' + file, points)
        else:
            for file in os.listdir('./paths'):
                if file != ".DS_Store":  # Problem while running on MacOS
                    if args.type == "S":
                        Spline_I.interpolate_with_spline('./paths/' + file, points)
                    else:
                        Lagrange.lagrange('./paths/' + file, points, cut=cut)
    elif args.file is not None and args.type is not None:
        if args.type == "S":
            Spline_I.interpolate_with_spline(args.file, points)
        elif args.type == "L":
            Lagrange.lagrange(args.file, points, cut=cut)
    elif args.file is not None:
        Lagrange.lagrange(args.file, points, cut=cut)
        Spline_I.interpolate_with_spline(args.file, points)
