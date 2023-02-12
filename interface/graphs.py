import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from simulator.battery import BatteryMeasurement

matplotlib.use("Qt5Agg")
plt.style.use("dark_background")


class BatPlotCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4):
        self.figure = Figure(figsize=(width, height))
        super().__init__(self.figure)
        self.setMinimumWidth(250)
        self.setMinimumHeight(250)


class BatTimeseriesCanvas(BatPlotCanvas):
    maxValues = 100

    def __init__(self, width=5, height=4):
        super().__init__(width, height)
        self.axes1 = self.figure.add_subplot(1, 3, 1)
        self.axes2 = self.figure.add_subplot(1, 3, 2)
        self.axes3 = self.figure.add_subplot(1, 3, 3)
        (self.line11,) = self.axes1.plot([], [])
        (self.line12,) = self.axes1.plot([], [])
        (self.line21,) = self.axes2.plot([], [])
        (self.line22,) = self.axes2.plot([], [])
        (self.line3,) = self.axes3.plot([], [])
        self.axes1.set_ylabel("Current $I(t)$ / A")
        self.axes2.set_ylabel("Voltage $V(t)$ / V")
        self.axes3.set_ylabel("SOC s(t) / 1")

    def appendValueToLine(self, line, axes, time: float, value: float):
        XY = line.get_xydata()
        XY = np.append(XY[-self.maxValues :], ((time, value),), axis=0)
        line.set_xdata(XY[:, 0])
        line.set_ydata(XY[:, 1])

    def addMeasurement(self, measurement: BatteryMeasurement):
        self.appendValueToLine(self.line11, self.axes1, measurement.time, measurement.current)
        self.appendValueToLine(self.line12, self.axes1, measurement.time, measurement.iR1)
        self.appendValueToLine(self.line21, self.axes2, measurement.time, measurement.voltage)
        self.appendValueToLine(self.line22, self.axes2, measurement.time, measurement.ocv)
        self.appendValueToLine(self.line3, self.axes3, measurement.time, measurement.soc)
        for axes in (self.axes1, self.axes2, self.axes3):
            axes.relim()
            axes.autoscale_view(True, True, True)
        self.draw()
