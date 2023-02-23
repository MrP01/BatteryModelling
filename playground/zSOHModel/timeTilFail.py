import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

plt.rcParams["text.usetex"] = True
##
#
# def scaleDegrading(current):
#     currentInC = current / 2.9
#     return np.clip(
#         1.61576599 - np.exp(0.88279821 * currentInC + -5.06803394),
#         0,
#         1,
#     )
#


def cycleAgeNoScaling(cycles):
    # Capacity is agnostic to units
    return max(2.9 * (1 - 4.58e-04 * cycles - np.exp(5.07e-02 * (cycles - 600))), 0)


def cycleAgeBattery(cycles, current):
    return cycleAgeNoScaling(cycles) * scaleDegrading(current)


def calAge(soc, timeInSeconds, temp=10):
    """
    Given an SOC that the battery is kept at, as well as the duration of storage,
    calculates the calendar aging that occurs
    """
    socFactor = (2 * soc - 1.3) ** 2 + 1
    if temp > 20:
        timeInMonths = 3.805e-7 * timeInSeconds
        return np.max(2.9 * (1 - 0.2 * timeInMonths * socFactor / 3), 0)
    else:
        timeInYears = 3.171e-8 * timeInSeconds
        return np.max(2.9 * (1 - 0.2 * timeInYears * socFactor), 0)


def scaleDegrading(current):
    """
    Returns the "current scaling factor" (s).
    s is defined by the relationship:
    Q(current) = s*Q(1C)

    Expected behaviour is as current increases, s decreases from 1 to 0.
    """
    if current == 0:
        return -1
    currentInC = current / 2.9
    return np.clip(
        1.01576599 - np.exp(0.88279821 * currentInC + -5.06803394),
        0,
        1,
    )


def totalScalingWithTime(cycles, current, soc=0.65, timeInSecs=1e7):
    """
    Given a number of cycles run for, with the current ran at,
    as well as battery aging time in seconds along with the (average) SOC
    that the battery is stored at, calculates degradation.
    """
    currentAgnosticCycleDegradationFactor = (
        2.9
        * 4.58e-04
        * cycles
        * (1 + (1 / 4.58e-04) * np.exp(5.07e-02 * (cycles - 700)))
    )
    currentScalingFactor = scaleDegrading(current)
    calendarDegradationFactor = 2.9 - calAge(soc, timeInSecs)
    if currentScalingFactor == -1:
        return 2.9 - calendarDegradationFactor
    else:
        cycleComponent = np.maximum(
            2.9
            - (
                # (1 - currentScalingFactor) * 2.9
                +(1 / currentScalingFactor)
                * currentAgnosticCycleDegradationFactor
            )
            - calendarDegradationFactor,
            0,
        )
        return cycleComponent


def objFun(n, current, threshold):
    return totalScalingWithTime(n, current) - 2.9 * threshold


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
currents = np.linspace(0.1, 15)
times = [getTotalDegradationTime(current, 0.8) for current in currents]
# # t = getTotalDegradationTime(2.9, 0.8)
plt.plot(currents, times, "r")
plt.title("Time of Failure for Different Currents")
plt.xlabel("Current (A)")
plt.ylabel("Times (s)")
plt.yscale("log")
plt.show()

##
def getBestCurrent(a, b, powerLaw, threshold, plotArg="n"):
    currents = np.linspace(1e-2, 15)
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
            f"Evaluation of Cost Function C with Death at {threshold}$Q_{{00}}$\n$p$ ={powerLaw}, Replacement Cost = {b:.2e}"
        )
        plt.xlabel("Current (A)")
        plt.ylabel("Net Utility")
        plt.legend([rf"$C = I^2t_f-RC \times \frac{1}{{t_f^p}}$"])
        plt.show()
    return currents[costFun.argmax()], costFun


replacementCost = 1e6
bc, cf = getBestCurrent(1, replacementCost, 1, 0.6, "y")

# print(getTotalDegradationTime(bc + 1, 0.8))
##
# laws = [0.5, 1, 2]

# laws = [0.5, 1, 2]

laws = [0.5, 1, 2]


def examinePowerlaw(laws):
    for law in laws:
        print(law)
        ratios = np.logspace(1, 7)
        bestCurs = [getBestCurrent(1, ratio, law, 0.6)[0] for ratio in ratios]
        print(bestCurs)
        plt.figure()
        plt.plot(ratios, bestCurs, "red")
        plt.xlabel("Replacement Cost")
        plt.ylabel("Best Current (A)")
        plt.legend([rf"$C = I^2t_f-RC \times \frac{1}{{t_f^p}}$"])
        plt.title(f"Best Currents as Functions of Replacement Cost\n$p$={law}")
        plt.xscale("log")
        plt.show()


examinePowerlaw(laws)
