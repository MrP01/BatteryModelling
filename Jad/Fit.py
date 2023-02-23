import numpy as np
import matplotlib.pylab as plt
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
from numpy import loadtxt


# https://www.electrogenic.co.uk/under-the-bonnet/technology/choosing-a-motor
def func1(X, a, b, c):
    x, y = X
    f = a * x + b * y + c
    return f


def func1p(X, a):
    x, y = X
    f = a[0][0] * x + a[0][1] * y + a[0][2]
    return f


def func2(X, a, b, c, d, e):
    x, y = X
    f = a * x + b * y + c + d * x * x + e * y * y
    return f


def func2p(X, a):
    x, y = X
    f = a[0][0] * x + a[0][1] * y + a[0][2] + a[0][3] * x * x + a[0][4] * y * y
    return f


def func3(X, a, b, c, d, e, f, g):
    x, y = X
    f = a * x + b * y + c + d * x * x + e * y * y + f * x * x * x + g * y * y * y
    return f


def func3p(X, a):
    x, y = X
    f = (
        a[0][0] * x
        + a[0][1] * y
        + a[0][2]
        + a[0][3] * x * x
        + a[0][4] * y * y
        + a[0][5] * x * x * x
        + a[0][6] * y * y * y
    )
    return f


def func2c(X, a, b, c, d, e, f):
    x, y = X
    f = a * x + b * y + c + d * x * x + e * y * y + f * x * y
    return f


def func2cp(X, a):
    x, y = X
    f = a[0][0] * x + a[0][1] * y + a[0][2] + a[0][3] * x * x + a[0][4] * y * y + a[0][5] * x * y
    return f


X = loadtxt("finalOutput.txt", usecols=0, delimiter=",", unpack=False)
Y = loadtxt("finalOutput.txt", usecols=4, delimiter=",", unpack=False)
xlin = np.linspace(X.min(), X.max(), 5)
ylin = np.linspace(Y.min(), Y.max(), int(Y.max() / Y.min()))
X = loadtxt("finalOutput.txt", usecols=0, delimiter=",", unpack=False)
Y = loadtxt("finalOutput.txt", usecols=4, delimiter=",", unpack=False)
columns = [1, 2, 3]
app = [1, 2, 3, 2]
counter2 = 0
print("Note: x is T and y is SOC")
for col in columns:
    fig = plt.figure()
    counter = 0
    counter2 = counter2 + 1
    if counter2 == 1:
        print("\nR0:\n")
        str2 = "R0"
    elif counter2 == 2:
        print("\nR1:\n")
        str2 = "R1"
    else:
        print("\nC:\n")
        str2 = "C"
    for ap in app:
        counter = counter + 1
        Z = loadtxt("finalOutput.txt", usecols=[col], delimiter=",", unpack=False)
        zlin = griddata((X, Y), Z, (xlin[None, :], ylin[:, None]), method="cubic")
        if counter == 1:
            f1 = func1
            f2 = func1p
            str = "ax+by+c:"
        elif counter == 2:
            f1 = func2
            f2 = func2p
            str = "ax+by+c+dx^2+ey^2:"
        elif counter == 3:
            f1 = func3
            f2 = func3p
            str = "ax+by+c+dx^2+ey^2+fx^3+gx^3:"
        else:
            f1 = func2c
            f2 = func2cp
            str = "ax+by+c+dx^2+ey^2+fxy:"
        a = curve_fit(f1, (X, Y), Z)
        Z2 = f2((X, Y), a)
        z2lin = griddata((X, Y), Z2, (xlin[None, :], ylin[:, None]), method="cubic")
        ax = fig.add_subplot(2, 2, counter, projection="3d")
        ax.set_title(str2)
        xig, yig = np.meshgrid(xlin, ylin)
        surf = ax.plot_surface(xig, yig, zlin, linewidth=0)
        surf2 = ax.plot_surface(xig, yig, z2lin, linewidth=0)
        z2 = np.logical_not(np.isnan(zlin - z2lin))
        print(str, a[0][:].round(6), "Error:", np.linalg.norm(Z - Z2) / np.mean(Z))
plt.show()
