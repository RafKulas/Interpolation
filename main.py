import os
import Lagrange
import Spline_I

if __name__ == "__main__":
    for file in os.listdir('./paths'):
        if file != ".DS_Store":
            print(file)
            Lagrange.lagrange('./paths/'+file, 100, True)
            # Spline_I.interpolate_with_spline('./paths/'+file, 100)
            print("done: " + file)


