import numpy as np
from scipy.optimize import fsolve


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
    root = fsolve(objFun, 10, args=[current, threshold])
    return root


def getTotalDegradationTime(current, threshold):
    """
    Current = current in Amperes
    Threshold = percentage of original Q_00 at which we claim battery is dead
    """
    numCyclesNeededToDegrade = getCyclesTilDegradedCapacity(current, threshold)
    print(np.ceil(numCyclesNeededToDegrade[0]))
    totalTimeNeeded = 0
    for i in range(1, int(numCyclesNeededToDegrade + 1)):
        totalTimeNeeded += cycleAgeBattery(i, current) / current
    return totalTimeNeeded


t = getTotalDegradationTime(2.9)
