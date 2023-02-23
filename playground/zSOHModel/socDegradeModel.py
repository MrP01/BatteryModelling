import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

plt.rcParams["text.usetex"] = True


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


def totalScalingWithTime(cycles, current, soc, timeInSecs):
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
    print(currentAgnosticCycleDegradationFactor)
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


def degradationScalingFactor(current):
    if np.array_equal(current, current * 0):
        print("h")
        return 0
    else:
        # Given a current, returns the factor by which it is
        # worse to run a battery than at 1C
        currentInC = current / 2.9
        return 1.01576599 + np.exp(0.88279821 * currentInC + -5.06803394)


def totalScaling(cycles, current):
    cycleCurrentScaling = np.maximum(
        2.9
        - (2.9 * 4.58e-04 * cycles + 2.9 * np.exp(5.07e-02 * (cycles - 600)))
        * degradationScalingFactor(current),
        0,
    )
    return cycleCurrentScaling


# def totalScalingWithTime(cycles, current, soc, timeInSecs):
#     cycleCurrentScaling = np.maximum(
#         2.9
#         - (2.9 * 4.58e-04 * cycles + 2.9 * np.exp(5.07e-02 * (cycles - 600)))
#         * degradationScalingFactor(current),
#         0,
#     )
#     return cycleCurrentScaling - (2.9 - calAge(soc, timeInSecs))


timeOfSit = 0.2e8
cycles = np.linspace(0, 600)
oneC = 2.9 * np.ones_like(cycles)
profile1C = [totalScalingWithTime(cycle, 2.9, 0.65, timeOfSit) for cycle in cycles]
profile1CShort = [
    totalScalingWithTime(cycle, 2.9, 0.65, 0.2 * timeOfSit) for cycle in cycles
]
profile0C = [totalScalingWithTime(cycle, 0 * 2.9, 0.65, timeOfSit) for cycle in cycles]
profile3C = [totalScalingWithTime(cycle, 3 * 2.9, 0.65, timeOfSit) for cycle in cycles]
profile4C = [totalScalingWithTime(cycle, 4 * 2.9, 0.65, timeOfSit) for cycle in cycles]
profile3CHighSOC = [
    totalScalingWithTime(cycle, 3 * 2.9, 0.9, timeOfSit) for cycle in cycles
]
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
##
twoC = 2 * 2.9 * np.ones_like(cycles)
threeC = 3 * 2.9 * np.ones_like(cycles)
fourC = 4 * 2.9 * np.ones_like(cycles)
fiveC = 5 * 2.9 * np.ones_like(cycles)
sixC = 6 * 2.9 * np.ones_like(cycles)
profile = totalScaling(cycles, oneC)
profile2 = totalScaling(cycles, twoC)
profile3 = totalScaling(cycles, threeC)
profile4 = totalScaling(cycles, fourC)
profile5 = totalScaling(cycles, fiveC)
profile6 = totalScaling(cycles, sixC)
plt.plot(cycles, profile, "r", label="1C")
plt.plot(cycles, profile2, "black", label="2C")
plt.plot(cycles, profile3, "g", label="3C")
plt.plot(cycles, profile4, "b", label="4C")
plt.plot(cycles, profile5, "orange", label="5C")
plt.plot(cycles, profile6, "magenta", label="6C")
plt.title("Plot of Capacity Against Cycle Number for Varying Currents")
plt.ylabel("Capacity (Ah)")
plt.xlabel("Cycle Number")
plt.legend(loc="upper right")
plt.show()
##
times = np.logspace(1, 8)
socs = 0.65 * np.ones_like(times)
ages = [calAge(0.65, time) for time in times]
plt.plot(times, ages)
plt.show()
