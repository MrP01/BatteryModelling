import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

plt.rcParams.update({"font.size": 16})
plt.rcParams["text.usetex"] = True
##
# This file generates a 'current scaling factor' CSF, NOT to be confused with
# the SOC, s. The variable CSF is a measure of how much further a battery's capacity Q(t)
# should degrade when ran at higher temperatures, compared to being run at 1C
# which we use as baseline. s takes a maximum at 1 when current is equal to 1C
# and a minimum of 0, which is effectively when using the battery at such a current
# would cause it to instantly die.
#
# We take results from:
# https://spiral.imperial.ac.uk/bitstream/10044/1/60288/6/Final_Manuscript__Characterization_of_the_Degradation_Process_of_Lithium_ion_Batteries_when_Discharged_at_Different_Current_Rates.pdf
# and adapt them to our usecase. This paper suggests we model the degradation process
# as a curve of the form
# f(t) = C1 * exp(a*t) + C2 exp(b*t)
# for constants C1,C2,a,b. We make the approximation that C1, C2 are agnostic to current
# and thus seek to find a(I), and b(I) via curve-fitting.

# Firstly, we fit a(I):

currentValuesInC = np.array([1, 2, 3])
aValues = np.array([-0.02905, -0.02896, -0.02093])


def cycleCurFit(x, a1, a2, a3):
    return a1 + np.exp(a2 * x + a3)


poptA, pcov = sp.optimize.curve_fit(
    cycleCurFit,
    currentValuesInC,
    aValues,
    p0=(-0.03, 3, -14),
)


def aFunc(current):
    return poptA[0] + np.exp(poptA[1] * current + poptA[2])


rangeOfCurrentValues = np.linspace(1, 3)
fittedAValues = cycleCurFit(rangeOfCurrentValues, *poptA)

plt.plot(currentValuesInC, aValues, "o", rangeOfCurrentValues, fittedAValues)
plt.title("Fit of $a$ against current")
plt.legend(["Raw data", "Fit data"])
plt.xlabel("Current (A)")
plt.ylabel("$a$ (1/cycles)")
plt.show()
##
# Next we seek to fit b(I)
bValues = np.array([-0.0001406, -0.0002115, -0.0003943])


def cycleCurFitBValues(x, a1, a2, a3):
    return a1 - np.exp(a2 * x + a3)


poptB, pcovB = sp.optimize.curve_fit(
    cycleCurFitBValues,
    currentValuesInC,
    bValues,
    p0=(-0.0003, 3, -14),
)


def bFunc(current):
    return poptB[0] - np.exp(poptB[1] * current + poptB[2])


rangeOfCurrentValues = np.linspace(1, 3)
fittedBValues = cycleCurFitBValues(rangeOfCurrentValues, *poptB)

plt.plot(currentValuesInC, bValues, "o", rangeOfCurrentValues, fittedBValues)
plt.title("Fit of $b$ against current")
plt.legend(["Raw data", "Fit data"])
plt.xlabel("Current (A)")
plt.ylabel("$b$ (1/cycles)")
plt.ticklabel_format(style="sci", scilimits=(-3, 4), axis="both")
plt.show()


##
# Now, having a(I) and b(I), we create a function to degrade capacity based on arbitrary current.
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
plt.ylabel("Capacity (Percentage of Initial)")
plt.legend(["1C", "2C", "3C"])
plt.show()
##
# Next, we find the ratios Q(I)/Q(1C) and plot these; these work only for
# 1C < I < 3C
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
# Then we construct a function to get the ratio Q(I)/Q(1C)
# for an arbitrary current. We then plot this function; this function
# returns the variable 'CSF'
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

rangeOfCurrentValues = np.linspace(0, 6)
yy = degradingFactor(rangeOfCurrentValues, *optimalDegradingFactorParameters)

plt.figure(figsize=(8, 6))
plt.tight_layout()
plt.plot(rangeOfCurrentValues[yy > 0] * 2.9, yy[yy > 0], "orange")
plt.title("Current Scaling Factor against Current")
plt.xlabel("Current (A)")
plt.ylabel("Current Scaling Factor")
# plt.legend(["actual data", "fit data"])
plt.show()


##
# To simply view results, either see the hardcoded comment below
# or run the code below after running all code above.
# Out[14]: array([ 1.01576599,  0.88279821, -5.06803394])
def scaleDegrading(current):
    currentInC = current / 2.9
    return np.clip(
        optimalDegradingFactorParameters[0]
        - np.exp(optimalDegradingFactorParameters[1] * currentInC + optimalDegradingFactorParameters[2]),
        0,
        1,
    )
