import numpy as np
import csv
from mat4py import loadmat
import matplotlib.pyplot as plt
import scipy as sp

plt.rcParams["text.usetex"] = True
##
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


##
# now checking degradation vs current draw
# last 2 entries are synthetic data, rest taken from plot

a = np.array([1, 2, 3])
b = np.array([-0.02905, -0.02896, -0.02093])


def cycleCurFit(x, a1, a2, a3):
    return a1 + np.exp(a2 * x + a3)


poptA, pcov = sp.optimize.curve_fit(
    cycleCurFit,
    a,
    b,
    p0=(-0.03, 3, -14),
)


def aFunc(current):
    return poptA[0] + np.exp(poptA[1] * current + poptA[2])


xx = np.linspace(1, 3)
yy = cycleCurFit(xx, *poptA)

plt.plot(a, b, "o", xx, yy)
plt.title("Fit of $a$ against current")
plt.legend(["Raw data", "Fit data"])
plt.xlabel("Current (A)")
plt.ylabel("$a$ (1/cycles)")
plt.show()
##
c = np.array([1, 2, 3])
d = np.array([-0.0001406, -0.0002115, -0.0003943])


def cycleCurFit2(x, a1, a2, a3):
    return a1 - np.exp(a2 * x + a3)


poptB, pcov = sp.optimize.curve_fit(
    cycleCurFit2,
    c,
    d,
    p0=(-0.0003, 3, -14),
)


def bFunc(current):
    return poptB[0] - np.exp(poptB[1] * current + poptB[2])


xx = np.linspace(1, 3)
yy = cycleCurFit2(xx, *poptB)

plt.plot(c, d, "o", xx, yy)
plt.title("Fit of $b$ against current")
plt.legend(["Raw data", "Fit data"])
plt.xlabel("Current (A)")
plt.ylabel("$b$ (1/cycles)")
# ax2 = plt.gca()
# fig2 = plt.gcf()
plt.show()
##
def degradeFunRaw(current, cycles):
    a = aFunc(current)
    b = bFunc(current)
    prefactor1 = 0.06108
    prefactor2 = 0.946
    return prefactor1 * np.exp(a * cycles) + prefactor2 * np.exp(b * cycles)


cycles = np.linspace(0, 300)
degradation1C = degradeFunRaw(1, cycles)
degradation2C = degradeFunRaw(2, cycles)
degradation25C = degradeFunRaw(2.5, cycles)
degradation28C = degradeFunRaw(2.8, cycles)
degradation3C = degradeFunRaw(3, cycles)


fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(cycles, degradation1C, "r")
ax1.plot(cycles, degradation2C, "g")
ax1.plot(cycles, degradation3C, "b")
ax1.set_title("Plot of raw degradation on supplementary data against current")
plt.xlabel("Current (A)")
plt.ylabel("Degradation (%)")
plt.legend(["1C", "2C", "3C"])
plt.show()
##
cycles = np.linspace(0, 300)
degradation2CRatio = degradation2C / degradation1C
degradation25CRatio = degradation25C / degradation1C
degradation28CRatio = degradation28C / degradation1C
degradation3CRatio = degradation3C / degradation1C


fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(cycles, degradation2CRatio, "r")
ax1.plot(cycles, degradation25CRatio, "g")
ax1.plot(cycles, degradation28CRatio, "b")
ax1.plot(cycles, degradation3CRatio, "orange")
ax1.set_title("Plot of raw degradation ratios")
plt.xlabel("Cycle count")
plt.ylabel("Degradation")
# plt.legend(["1C", "2C", "3C"])
plt.show()
##
x = [2, 2.25, 2.5, 2.8, 3]
degradationRatios = [
    0.9789551462062951,
    0.9699102891582062,
    0.9585703864308819,
    0.9411715241181353,
    0.926830315358507,
]


def degradingFactor(current, a1, a2, a3):
    return a1 - np.exp(a2 * current + a3)


optimalDegradingFactorParameters, pcov = sp.optimize.curve_fit(
    degradingFactor,
    x,
    degradationRatios,
    p0=(1, 3, -1),
)

xx = np.linspace(0, 6)
yy = degradingFactor(xx, *optimalDegradingFactorParameters)

plt.plot(xx * 2.9, yy, "orange")
plt.title("Degradation Ratios against Current")
plt.xlabel("Current (A)")
plt.ylabel("Degradation Ratio")
# plt.legend(["actual data", "fit data"])
plt.show()
##
# Out[14]: array([ 1.01576599,  0.88279821, -5.06803394])
def scaleDegrading(current):
    currentInC = current / 2.9
    return np.clip(
        optimalDegradingFactorParameters[0]
        - np.exp(
            optimalDegradingFactorParameters[1] * currentInC
            + optimalDegradingFactorParameters[2]
        ),
        0,
        1,
    )


def calAge(initialCapacity, timeInSeconds, temp=25):
    # Capacity is agnostic to units
    if temp > 20:
        timeInMonths = 3.805e-7 * timeInSeconds
        return max(initialCapacity * (1 - 0.2 * timeInMonths / 3), 0)
    else:
        timeInYears = 3.171e-8 * timeInSeconds
        return max(initialCapacity * (1 - 0.2 * timeInYears), 0)


def cycleAgeNoScaling(cycles):
    # Capacity is agnostic to units
    return max(2.9 * (1 - 4.58e-04 * cycles - np.exp(5.07e-02 * (cycles - 600))), 0)


def ageBat(totNumCycles, timeElapsed, tempUsed):
    # Reasoning is cyclic aging occurs on a much shorter timescale and thus impacts the battery 'first'
    # We then use this degraded capacity to calculate any calendar aging that has occurred
    cycleAgingDegradedCapacity = cycleAgeNoScaling(totNumCycles)
    totalDegradedCapacity = calAge(cycleAgingDegradedCapacity, timeElapsed, tempUsed)
    return totalDegradedCapacity


def cycleAgeBattery(cycles, current):
    return cycleAgeNoScaling(cycles) * scaleDegrading(current)


cycleAgeBattery(300, 2)
