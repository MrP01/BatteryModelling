import matplotlib.pyplot as plt
import numpy as np

# plt.rcParams.update({"font.size": 16})
# plt.rcParams["text.usetex"] = True
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
    socFactor = np.cosh(0.4 * soc - 0.15)  # (1.5 * soc - 0.5) ** 4 + 1
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
    CSF = currentScalingFactor(current)
    CDF = 2.9 - calendarDegradationFactor(soc, timeInSecs)
    if CSF == -1:
        return 2.9 - CDF
    else:
        # To view background for CACDF view:
        # 'generateCurrentAgnosticDegradation.py'
        CACDF = 2.9 * 4.58e-04 * cycles * (1 + (1 / 4.58e-04) * np.exp(5.07e-02 * (cycles - 700)))
        print(CACDF)
        capacityAfterDegradation = np.maximum(
            2.9 - (CACDF / CSF) - CDF,
            0,
        )
        return capacityAfterDegradation


# The code above is all that is needed for our degradation model.


# This next code just generating capacity profiles for different current profiles
def generatePlots():
    timeOfSit = 0.2e8
    cycles = np.linspace(0, 600)
    profile0C = [totalDegradation(cycle, 0, 0.65, timeOfSit) for cycle in cycles]
    profile1C = [totalDegradation(cycle, 2.9, 0.65, timeOfSit) for cycle in cycles]
    profile1CShort = [totalDegradation(cycle, 2.9, 0.65, 0.2 * timeOfSit) for cycle in cycles]
    profile3C = [totalDegradation(cycle, 3 * 2.9, 0.65, timeOfSit) for cycle in cycles]
    profile4C = [totalDegradation(cycle, 4 * 2.9, 0.65, timeOfSit) for cycle in cycles]
    # profile3CHighSOC = [totalDegradation(cycle, 3 * 2.9, 0.95, timeOfSit) for cycle in cycles]

    hours = timeOfSit / 3600
    days = hours / 24

    plt.figure()
    # plt.tight_layout()
    plt.plot(cycles, profile1C, "r", label=f"$I = 1C$, Time = {days:.2f} days")
    plt.plot(cycles, profile1CShort, "g", label=f"$I = 1C$, Time = {0.5*days:.2f} days")
    plt.plot(cycles, profile3C, "m", label=f"$I = 3C$, Time = {days:.2f} days")
    plt.plot(cycles, profile4C, "cyan", label=f"$I = 4C$, Time = {days:.2f} days")
    plt.plot(cycles, profile0C, "b", label=f"$I = 0C$, Time = {days:.2f} days")
    plt.legend(loc="best")
    plt.title("Comparison of Current and Aging Profiles with Cycles on Capacity")
    plt.xlabel("Cycles")
    plt.grid(visible=True, which="major", c="#dddddd", lw=2, ls="-")
    plt.ylabel("Capacity (Ah)")
    plt.savefig("figure.pdf")
    plt.show()
    return profile0C


x = generatePlots()


##
def generateDQPlot():
    socs = np.linspace(0, 1, 200)
    dvals = -0.4 * abs(np.sinh(0.4 * socs - 0.15))
    plt.figure(figsize=(8, 6))
    plt.tight_layout()
    plt.plot(socs, dvals, "r")
    plt.legend(loc="best")
    plt.title("$(Q_s)_{t,T,I}$ against $s$")
    plt.xlabel("$s$")
    plt.grid(visible=True, which="major", c="#dddddd", lw=2, ls="-")
    plt.ylabel("$(Q_s)_{t,T,I}$ (Ah)")
    plt.show()
    return


# generateDQPlot()
