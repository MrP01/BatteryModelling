import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

plt.rcParams["text.usetex"] = True


def scaleDegrading(current):
    currentInC = current / 2.9
    return np.clip(
        1.01576599 - np.exp(0.88279821 * currentInC + -5.06803394),
        0,
        1,
    )


def cycleAgeNoScaling(cycles):
    # Capacity is agnostic to units
    return max(2.9 * (1 - 4.58e-04 * cycles - np.exp(5.07e-02 * (cycles - 600))), 0)


def cycleAgeBattery(cycles, current):
    return cycleAgeNoScaling(cycles) * scaleDegrading(current)


def objFun(n, current, threshold):
    return cycleAgeBattery(n, current) - 2.9 * threshold


def getCyclesTilDegradedCapacity(current, threshold):
    root = fsolve(objFun, 10, args=(current, threshold))
    return root


def getTotalDegradationTime(current, threshold):
    """
    Current = current in Amperes
    Threshold = percentage of original Q_00 at which we claim battery is dead
    """
    numCyclesNeededToDegrade = getCyclesTilDegradedCapacity(current, threshold)
    # print(np.ceil(numCyclesNeededToDegrade[0]))
    totalTimeNeeded = 0
    for i in range(1, int(numCyclesNeededToDegrade + 1)):
        totalTimeNeeded += cycleAgeBattery(i, current) / current
    return totalTimeNeeded


#
# currents = np.linspace(0, 15)
# times = [1 / getTotalDegradationTime(current, 0.8) for current in currents]
# # t = getTotalDegradationTime(2.9, 0.8)
# plt.plot(currents, times)
# plt.show()

##
def getBestCurrent(a, b, powerLaw, threshold, plotArg="n"):
    currents = np.linspace(1e-4, 15)
    times = np.array(
        [getTotalDegradationTime(current, threshold) for current in currents]
    )

    with np.errstate(divide="ignore"):
        inverseTimes = np.divide(1, times) ** powerLaw
    costFun = (
        a
        * np.multiply(
            np.square(currents[0 : len(inverseTimes)]), times[0 : len(inverseTimes)]
        )
        - b * inverseTimes
    )
    if plotArg == "y":
        print(f"Best current is {currents[costFun.argmax()]:.1f}A")
        if np.max(costFun) < 0:
            print("You are at a net DETRIMENT")
        elif np.max(costFun) == 0:
            print("You are NEUTRAL")
        else:
            print("You are at a net POSIITVE")
        plt.plot(currents, costFun, "red")
        plt.title(
            f"Evaluation of Cost Function C with Death at {threshold}$Q_{{00}}$\np ={powerLaw}, Ratio of Benefit = {b:.2e}"
        )
        plt.xlabel("Current")
        plt.ylabel("Net Utility")
        plt.legend([rf"$C = I^2t_f-RoB \times \frac{1}{{t_f^p}}$"])
        plt.show()
    return currents[costFun.argmax()], costFun


ratioOfBenefit = 1e6
bc, cf = getBestCurrent(1, ratioOfBenefit, 1, 0.8, "y")
##
laws = [0.5, 1, 2]


def examinePowerlaw(laws):
    for law in laws:
        print(law)
        ratios = np.logspace(3, 5.5, 100)
        bestCurs = [getBestCurrent(1, ratio, law, 0.8)[0] for ratio in ratios]
        print(bestCurs)
        plt.figure()
        plt.plot(ratios, bestCurs, "red")
        plt.xlabel("RoB")
        plt.ylabel("Best Current")
        plt.legend([rf"$C = I^2t_f-RoB \times \frac{1}{{t_f^p}}$"])
        plt.title(f"Best Currents as Functions of Ratio of Benefit\np={law}")
        plt.show()


examinePowerlaw(laws)
