import numpy as np
import csv
from mat4py import loadmat
import matplotlib.pyplot as plt

##
data = loadmat("pulses.mat")
time = np.array(data["meas"]["Time"])
voltage = np.array(data["meas"]["Voltage"])
current = np.array(data["meas"]["Current"]) * -1
ah = np.array(data["meas"]["Ah"]) * -1
##
fig1, (ax1) = plt.subplots(figsize=(10, 4))
ax1.plot(time, voltage)
ax1.set_title("V against T")
plt.show()
##
fig2, (ax2) = plt.subplots()
ax2.plot(time, current)
ax2.set_title("I against T")
plt.show()
##
fig3, (ax3) = plt.subplots()
ax3.plot(time, ah)
ax3.set_title("Ah against T")
plt.show()
##
nonzeroIndicesOfCurrent = np.nonzero(current)[0]
indicesOfChange = np.where(nonzeroIndicesOfCurrent[:-1] != np.subtract(nonzeroIndicesOfCurrent[1:], 1))[0]
# indicesOfChange = [100,201,...6488]
# these are the
currentGroupsInit = nonzeroIndicesOfCurrent[0 : indicesOfChange[0] + 1]

currentGroups = [nonzeroIndicesOfCurrent[indicesOfChange[i] + 1 : indicesOfChange[i + 1] + 1] for i in range(57)]
currentGroups.insert(0, currentGroupsInit)
##
indexOffset = 50
groupNumber = 57  # max of 65
fig, (ax) = plt.subplots(figsize=(10, 4))
ax.plot(
    time[currentGroups[groupNumber][0] - int(indexOffset / 2) : currentGroups[groupNumber][-1] + indexOffset],
    voltage[currentGroups[groupNumber][0] - int(indexOffset / 2) : currentGroups[groupNumber][-1] + indexOffset],
)
ax.set_title(f"V against T, group number {groupNumber}")
plt.show()
##
for groupIndex in range(58):
    voltageName = f"voltage{groupIndex}"
    currentName = f"current{groupIndex}"
    ahName = f"ah{groupIndex}"
    timeName = f"time{groupIndex}"

    workingVoltage = voltage[
        currentGroups[groupIndex][0] - int(indexOffset / 2) : currentGroups[groupIndex][-1] + indexOffset
    ]

    workingCurrent = current[
        currentGroups[groupIndex][0] - int(indexOffset / 2) : currentGroups[groupIndex][-1] + indexOffset
    ]

    workingAh = 1 - (
        ah[currentGroups[groupIndex][0] - int(indexOffset / 2) : currentGroups[groupIndex][-1] + indexOffset] / 2.9
    )

    flatVoltage = [item for sublist in workingVoltage for item in sublist]
    flatCurrent = [item for sublist in workingCurrent for item in sublist]
    flatAh = [item for sublist in workingAh for item in sublist]
    with open(f"./cleanData/run{groupIndex+1}_10C.csv", "w") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["voltage", "current", "SOC"])
        wr.writerows(zip(flatVoltage, flatCurrent, flatAh))
        # wr.writerow(flatVoltage)
        # wr.writerow(flatCurrent)
##
