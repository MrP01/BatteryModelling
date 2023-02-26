import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("cleanData/25c/cleanData25C/run5_25C.csv")
normalisedVoltage = df.voltage - df.voltage.min() + 0.01
Vprime = np.diff(normalisedVoltage)

firstSpikeIndex = np.argmin(Vprime)
secondSpikeIndex = firstSpikeIndex + (np.argmax(Vprime) - firstSpikeIndex) // 8

firstSection = np.array(normalisedVoltage[firstSpikeIndex:secondSpikeIndex])
secondSection = np.array(normalisedVoltage[secondSpikeIndex:])
firstX = range(len(firstSection))
secondX = range(len(secondSection))

firstCurveParams = np.polyfit(firstX, np.log(firstSection), 1)
secondCurveParams = np.polyfit(secondX, np.log(secondSection), 1)

fig = plt.figure()
axes: matplotlib.axes.Axes = fig.add_subplot(2, 1, 1)
axes.plot(firstX, firstSection)
axes.plot(firstX, np.exp(firstCurveParams[1] * firstX + firstCurveParams[0]))
# axes: matplotlib.axes.Axes = fig.add_subplot(2, 1, 2)
# axes.plot(secondX, secondSection)
# axes.plot(secondX, np.exp(secondCurveParams[0] * secondX + secondCurveParams[1]))
# axes.set_xlabel("$i$")
# axes.set_ylabel("$V(t_i)$")
# fig.savefig(str(RESULTS / "plot.png"))
plt.show()
