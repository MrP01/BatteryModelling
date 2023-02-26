import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
# This file outlines the degradation model we use. There are
# several components to the model. The overall function looks something like:
# Q(cycles,current,SOC,time) = Q_0 - (CACDF(cycles)/CSF(current)) - CDF(SOC,time)
# Where:
# - Q_0: Initial capacity (2.9Ah)
# - CACDF(cycles) (Current Agnostic Cycle Degradation Factor): A function which is derived
#   from curve fitting the degradation of capacity from the cell's datasheet for a SINGLE current
# - CSF(current) (Current Scaling Factor): A function which, for a given input current, returns
#   a variable which relates how much further to degrade the capacity of cell based on the
#   input current. CSF(<1C) is always 1, as we expect no extraneous degradation in this case.
#   CSF reaches a minimum value of 0, at which point the term CACDF/CSF blows up,
#   and we expect the battery to instantly die; this is expected behaviour at high enough capacity.
# - CDF(SOC,time) (Calendar Degradation Factor): A function which returns a degradation in capacity
#   for a given time period and a given (average) SOC that the battery has been kept at whilst not
#   in use. NOTE: THIS FUNCTION HAS AN OPTIONAL TEMPERATURE ARGUMENT WHICH IS CURRENTLY NOT USED


def calendarDegradationFactor(soc, timeInSeconds, temp=10):
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


def currentScalingFactor(current):
    """
    Returns the "current scaling factor" (CSF).
    See 'currentScalingFunction.py' for details.
    Expected behaviour is as current increases, CSF decreases from 1 to 0.
    """
    if current == 0:
        return -1
    currentInC = current / 2.9
    return np.clip(
        1.01576599 - np.exp(0.88279821 * currentInC + -5.06803394),
        0,
        1,
    )


def totalDegradation(cycles, current, soc=0.65, timeInSecs=1e7):
    """
    Given a number of cycles run for, with the current ran at,
    as well as battery aging time in seconds along with the (average) SOC
    that the battery is stored at, calculates degradation.

    # Q(cycles,current,SOC,time) = Q_0 - (CACDF(cycles)/CSF(current)) - CDF(SOC,time)
    """
    # To view background for CACDF view:
    # 'generateCurrentAgnosticDegradation.py'
    CACDF = 2.9 * 4.58e-04 * cycles * (1 + (1 / 4.58e-04) * np.exp(5.07e-02 * (cycles - 700)))
    CSF = currentScalingFactor(current)
    CDF = 2.9 - calendarDegradationFactor(soc, timeInSecs)
    if currentScalingFactor == -1:
        return 2.9 - CDF
    else:
        capacityAfterDegradation = np.maximum(
            2.9 - (CACDF / CSF) - CDF,
            0,
        )
        return capacityAfterDegradation


# The code above is all that is needed for our degradation model.
#######
# This next code just generating capacity profiles for different current profiles
def generatePlots():
    timeOfSit = 0.2e8
    cycles = np.linspace(0, 600)
    profile1C = [totalDegradation(cycle, 2.9, 0.65, timeOfSit) for cycle in cycles]
    profile1CShort = [totalDegradation(cycle, 2.9, 0.65, 0.2 * timeOfSit) for cycle in cycles]
    profile0C = [totalDegradation(cycle, 0 * 2.9, 0.65, timeOfSit) for cycle in cycles]
    profile3C = [totalDegradation(cycle, 3 * 2.9, 0.65, timeOfSit) for cycle in cycles]
    profile4C = [totalDegradation(cycle, 4 * 2.9, 0.65, timeOfSit) for cycle in cycles]
    profile3CHighSOC = [totalDegradation(cycle, 3 * 2.9, 0.9, timeOfSit) for cycle in cycles]
    plt.plot(cycles, profile1C, "r", label=f"1C Time={timeOfSit:.2e}s")
    plt.plot(cycles, profile1CShort, "g", label=f"1C Time={0.5*timeOfSit:.2e}s")
    plt.plot(cycles, profile0C, "b", label=f"0C Time={timeOfSit:.2e}")
    plt.plot(cycles, profile3C, "magenta", label=f"3C Time={timeOfSit:.2e}")
    plt.plot(cycles, profile4C, "cyan", label=f"4C Time={timeOfSit:.2e}")
    plt.plot(cycles, profile3CHighSOC, "orange", label=f"3C, High SOC Time={timeOfSit:.2e}")
    plt.legend(loc="best")
    plt.title("Comparison of Current and Aging Profiles with Cycles on Capacity")
    plt.xlabel("Cycles")
    plt.ylabel("Capacity (Ah)")
    plt.show()


generatePlots()
