import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from interface.batmap import BatMap
from interface.graphs import BatPlotCanvas
from simulator.simulation import Simulation


class MainWindow(Simulation, QtWidgets.QWidget):
    """Our Main Window Class that hosts all sub-widgets and has overall control over the GUI.
    All the simulation-related graphical items and code should be located in simulator/ to keep
    this file as short and clean as possible.
    """

    def __init__(self):
        super().__init__()
        self.batmap = BatMap(self.batgraph, self.batmobile, self)

    def iterate(self):
        super().iterate()
        self.batmap.render()

    def updatePlots(self):
        self.voltageGraph.axes.plot(np.linspace(0, 20), 1 - np.linspace(0, 1) + 0.3 * (np.random.random((50,)) - 1))
        # self.voltageGraph.axes.set_xlabel("Time $t$ / s")
        self.voltageGraph.axes.set_ylabel("Voltage $V(t)$ / V")
        self.currentGraph.axes.plot(np.linspace(0, 20), 1 - np.linspace(0, 1) + 0.3 * (np.random.random((50,)) - 1))
        # self.currentGraph.axes.set_xlabel("Time $t$ / s")
        self.currentGraph.axes.set_ylabel("Current $I(t)$ / A")
        self.socGraph.axes.plot(np.linspace(0, 20), 1 - np.linspace(0, 1) + 0.3 * (np.random.random((50,)) - 1))
        # self.socGraph.axes.set_xlabel("Time $t$ / s")
        self.socGraph.axes.set_ylabel("State of Charge s(t) / 1")

    def startOrStop(self):
        if self.controlBtn.text() == "Start":
            self.iterationTimerId = self.startTimer(20)
            self.controlBtn.setText("Stop")
        else:
            self.killTimer(self.iterationTimerId)
            self.controlBtn.setText("Start")

    def timerEvent(self, event: QtCore.QTimerEvent):
        self.iterate()
        return super().timerEvent(event)

    def buildUI(self):
        self.controlBtn = QtWidgets.QPushButton("Start", self)
        self.controlBtn.clicked.connect(self.startOrStop)  # type: ignore

        self.voltageGraph = BatPlotCanvas()
        self.currentGraph = BatPlotCanvas()
        self.socGraph = BatPlotCanvas()

        self.batmap.render()
        self.updatePlots()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.batmap, 0, 0)
        layout.addWidget(self.controlBtn, 0, 1)
        graphLayout = QtWidgets.QHBoxLayout()
        graphLayout.addWidget(self.currentGraph)
        graphLayout.addWidget(self.voltageGraph)
        graphLayout.addWidget(self.socGraph)
        # graphLayout.addStretch()
        layout.addLayout(graphLayout, 1, 0)
        self.setLayout(layout)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W:
            self.close()
        if event.key() == Qt.Key.Key_S:
            self.startOrStop()
        return super().keyPressEvent(event)
