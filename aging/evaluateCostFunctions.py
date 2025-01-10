from typing import NoReturn

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

import aging.degradationModel as dm

plt.rcParams.update({"font.size": 16})
plt.rcParams["text.usetex"] = True
# This file lets us evaluate some basic cost functions and
# also lets us generate any optimal currents for some specific cost functions.


def objFun(n, current, threshold):
    return dm.totalDegradation(n, current) - 2.9 * threshold


def getCyclesTilDegradedCapacity(current, threshold):
    return fsolve(objFun, 10, args=(current, threshold))


def getTotalDegradationTime(current, threshold):
    """Current = current in Amperes
    Threshold = percentage of original Q_00 at which we claim battery is dead.
    """
    numCyclesNeededToDegrade = getCyclesTilDegradedCapacity(current, threshold)
    totalTimeNeeded = 0
    for i in range(1, int(numCyclesNeededToDegrade + 1)):
        totalTimeNeeded += dm.totalDegradation(i, current, 0.65, 0) / current
    return totalTimeNeeded


currents = np.linspace(0.1, 15)
times = [getTotalDegradationTime(current, 0.8) for current in currents]
plt.plot(currents, times, "r")
plt.title("Time of Failure for Different Currents")
plt.xlabel("Current (A)")
plt.ylabel("Times (s)")
plt.yscale("log")
plt.show()


##
def getBestCurrent(a, b, powerLaw, threshold, plotArg="n"):
    currents = np.linspace(1e-2, 15)
    times = np.array([getTotalDegradationTime(current, threshold) for current in currents])

    with np.errstate(divide="ignore"):
        inverseTimes = np.divide(1, times) ** powerLaw
    costFun = (
        a * np.multiply(np.square(currents[0 : len(inverseTimes)]), times[0 : len(inverseTimes)]) - b * inverseTimes
    )
    if plotArg == "y":
        if np.max(costFun) < 0 or np.max(costFun) == 0:
            pass
        else:
            pass

        plt.figure(figsize=(9, 6))
        plt.tight_layout()
        plt.plot(currents, costFun, "red")
        plt.title(
            f"Evaluation of Cost Function C with Death at {threshold}$Q_{{00}}$\n$p$ ={powerLaw}, "
            f"Replacement Cost = {b:.2e}",
        )
        plt.xlabel("Current (A)")
        plt.ylabel("Net Utility")
        plt.legend([rf"$C = I^2t_f-RC \times \frac{1}{{t_f^p}}$"])
        plt.show()
    return currents[costFun.argmax()], costFun


replacementCost = 12e5
bc, cf = getBestCurrent(1, replacementCost, 1, 0.7, "y")

##
laws = [0.5, 1, 2]


def examinePowerlaw(laws) -> None:
    for law in laws:
        ratios = np.logspace(1, 7)
        bestCurs = [getBestCurrent(1, ratio, law, 0.6)[0] for ratio in ratios]
        plt.figure()
        plt.plot(ratios, bestCurs, "red")
        plt.xlabel("Replacement Cost")
        plt.ylabel("Best Current (A)")
        plt.legend([rf"$C = I^2t_f-RC \times \frac{1}{{t_f^p}}$"])
        plt.title(f"Best Currents as Functions of Replacement Cost\n$p$={law}")
        plt.xscale("log")
        plt.show()


examinePowerlaw(laws)


def cycleAgeBattery(cycle, current) -> NoReturn:
    raise NotImplementedError
