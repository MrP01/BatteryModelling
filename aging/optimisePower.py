import evaluateCostFunctions as ttf
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate


def getModelParams():  # Should read from file but I am just copying from other program--parameterCurveFinding.py
    # in nickWeek3
    R0 = np.array(
        [
            0.99055269,
            -2.26465394,
            1.93048217,
            -0.95348885,
            0.52165477,
            -0.24699246,
            0.08733394,
        ],
    )
    R1 = np.array(
        [
            24.93391031,
            -89.92504695,
            130.05284213,
            -96.30378232,
            38.4476705,
            -7.8265193,
            0.64865373,
        ],
    )
    C1 = np.array(
        [
            -839658.33428892,
            2121361.97592949,
            -2065305.40823765,
            906760.09622885,
            -101216.29866021,
        ],
    )
    OCV = np.array([10.59735953, -33.51599917, 40.16840115, -22.18084932, 6.28065451, 2.80646924])
    return R0, R1, C1, OCV


def computePowerAtGivenCycle(current, cycle, R0, R1, C1, OCV, operationBand=None):
    if operationBand is None:
        operationBand = [1, 0.2]
    Qn = ttf.cycleAgeBattery(cycle, current)

    def V(SOC):
        return np.polyval(OCV, SOC) - current * np.polyval(R0, SOC) - current * np.polyval(R1, SOC)

    def SOCTransform(t):
        return 1 - current / Qn * t

    startTime = -Qn / current * (operationBand[0] - 1)
    endTime = -Qn / current * (operationBand[1] - 1)

    def VTransformed(t):
        return V(SOCTransform(t))

    return current * integrate.quad(VTransformed, startTime, endTime)[0]


def computePower(current, threshold=0.8):
    # print("*"*10)
    # print("Power computing for current = " + str(current))
    finalCycle = ttf.getCyclesTilDegradedCapacity(current, threshold)
    # print("Cycles undergone: " + str(np.floor(finalCycle)))
    R0, R1, C1, OCV = getModelParams()
    P = 0
    for i in range(int(np.floor(finalCycle))):  # i = k means integrate over the (k+1)th
        P += computePowerAtGivenCycle(current, i, R0, R1, C1, OCV)
    P += computePowerAtGivenCycle(current, np.floor(finalCycle), R0, R1, C1, OCV) * (finalCycle - np.floor(finalCycle))
    # print("Total power: "+str(P))
    return P


if __name__ == "__main__":
    current = 1
    Q = 2.9
    R0, R1, C1, OCV = getModelParams()
    x = np.linspace(0.01, 20, 51)
    y = np.zeros(51)
    for i in range(len(x)):
        y[i] = computePower(x[i])
    plt.plot(x, y)
    plt.show()
