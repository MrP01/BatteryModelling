from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThreadPool

from interface.batmap import BatMap
from interface.graphs import BatTimeseriesCanvas
from simulator.simulation import Simulation


class MainWindow(Simulation, QtWidgets.QWidget):
    """Our Main Window Class that hosts all sub-widgets and has overall control over the GUI.
    All the simulation-related graphical items and code should be located in simulator/ to keep
    this file as short and clean as possible.
    """

    STEPS_PER_FRAME = 20

    def __init__(self):
        super().__init__()
        self.batmap = BatMap(self.batgraph, self.batmobile, self)
        self.threadPool = QThreadPool()
        self.setWindowTitle("Battery Modelling in the BatMobile")

    def iterate(self):
        super().iterate()  # calls the Simulation class's numerical integration step
        self.batmap.render()
        self.statsLabel.setText(
            f"Position: {self.batmobile.position:.2f}\n"
            f"Velocity: {self.batmobile.velocity:.2f}\n"
            f"Acceleration: {self.batmobile.acceleration:.2f}"
        )

        if self.step % self.STEPS_PER_FRAME == 0:
            self.updatePlots()

    def updatePlots(self):
        """Updates the plots and redraws them. This is an expensive operation, so we run it outside the main thread."""
        measurement = self.batmobile.battery.measurement()
        measurement.time = self.totalTimeElapsed
        self.threadPool.start(lambda: self.batteryPlots.addMeasurement(measurement))

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
        self.resetBtn = QtWidgets.QPushButton("Reset", self)
        self.exportBtn = QtWidgets.QPushButton("Export", self)
        usageLabel = QtWidgets.QLabel(
            "Controls:\n"
            "Press 'Start' to begin the simulation.\n"
            "Use Up/Down arrow keys to steer.\n"
            "Press 'H' to halt the car.\n"
            "Press 'S' as a shortcut to start/stop."
        )
        self.statsLabel = QtWidgets.QLabel()
        self.controlBtn.clicked.connect(self.startOrStop)  # type: ignore

        self.batteryPlots = BatTimeseriesCanvas()

        self.batmap.render()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.batmap, 0, 0)
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(self.controlBtn)
        buttonLayout.addWidget(self.resetBtn)
        buttonLayout.addWidget(self.exportBtn)
        buttonLayout.addWidget(usageLabel)
        buttonLayout.addWidget(self.statsLabel)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout, 0, 1)
        graphLayout = QtWidgets.QHBoxLayout()
        graphLayout.addWidget(self.batteryPlots)
        # graphLayout.addStretch()
        layout.addLayout(graphLayout, 1, 0, 1, 2)
        self.setLayout(layout)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W:
            self.close()
        if event.key() == Qt.Key.Key_S:
            self.startOrStop()
        return super().keyPressEvent(event)
