import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["text.usetex"] = True


def cdf(soc, timeInSeconds, temp=10):
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


socs = np.linspace(0, 1)

cdfvals = [cdf(soc, 1e6) for soc in socs]
##
plt.plot(socs, cdfvals)
plt.show()
