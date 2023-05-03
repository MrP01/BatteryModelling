import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

plt.rcParams["text.usetex"] = True
# This function takes data from the cell's degradation curve as a function
# of cycles, and fits that data to a curve to be used within a function.

# last 2 entries are synthetic data, rest taken from plot
x = np.array([0, 100, 200, 260, 300, 400, 500, 575, 590])
y = np.array([2.9, 2.75, 2.56, 2.5, 2.45, 2.38, 2.31, 1.25, 0.25])


fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(x, y, "o")
ax1.set_title("Q_0 against C, synthetic tail")
plt.show()


def exponentialFit(x, b, c, d):
    return 2.9 * (1 - d * x - np.exp(b * (x - c)))


popt, pcov = sp.optimize.curve_fit(exponentialFit, x, y, p0=(1 / 600, 300, 1 / 2000))
# Best values for b,c,d:
# b = 5.07e-02
# c = 600
# d = 4.58e-04

xx = np.linspace(10, 600, 1000)
yy = exponentialFit(xx, *popt)

plt.plot(x, y, "o", xx, yy)
plt.title("fit of Q_0 against C with synthetic tail")
plt.legend(["actual data", "fit data"])
ax2 = plt.gca()
fig2 = plt.gcf()
plt.show()
