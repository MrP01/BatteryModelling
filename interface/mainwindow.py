from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThreadPool

from interface.batmap import BatMap
from interface.graphs import BatTimeseriesCanvas
from simulator.simulation import Simulation


NUMERICAL_KEYS = (Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4, Qt.Key.Key_5)


class MainWindow(Simulation, QtWidgets.QWidget):
    """Our Main Window Class that hosts all sub-widgets and has overall control over the GUI.
    All the simulation-related graphical items and code should be located in simulator/ to keep
    this file as short and clean as possible.
    """

    STEPS_PER_FRAME = 15

    def __init__(self):
        super().__init__()
        self.batmap = BatMap(self.batgraph, self.batmobile, self)
        self.setWindowTitle("Battery Modelling in the BatMobile")
        self.threadPool = QThreadPool()
        self.userSelectedTurnIndex = None

    def iterate(self):
        if (
            self.userSelectedTurnIndex is None
            and self.batmobile.position >= self.batgraph.edges[self.currentEdge()]["distance"]
        ):
            print("Turning time")
            self.turnLabel.setText("Where would you like to turn? Press 1, 2, 3, etc.")
            self.turnLabel.setHidden(False)
            self.startOrStop()
            return
        super().iterate()  # calls the Simulation class's numerical integration step
        self.batmap.render()
        self.statsLabel.setText(
            f"Time: {self.totalTimeElapsed:.2f} s\n"
            f"Position: {self.batmobile.position:.2f} m\n"
            f"Velocity: {self.batmobile.velocity:.2f} m/s\n"
            f"Acceleration: {self.batmobile.acceleration:.2f} m/s²\n"
            f"Motor Consumption: {self.batmobile.P_motor:.2f} W"
        )

        if self.step % self.STEPS_PER_FRAME == 1:
            self.updatePlots()

    def updatePlots(self):
        """Updates the plots and redraws them. This is an expensive operation, so we run it outside the main thread."""
        measurement = self.batmobile.battery.measurement()
        measurement.time = self.totalTimeElapsed
        # self.batteryPlots.addMeasurement(measurement)
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
            "Click 'Start' to begin the simulation.\n"
            "Use Up/Down arrow keys to drive.\n"
            "Press 'H' to halt the car.\n"
            "Press 'S' as a shortcut to start/stop."
        )
        self.statsLabel = QtWidgets.QLabel()
        self.turnLabel = QtWidgets.QLabel()
        self.turnLabel.setHidden(True)
        self.turnLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.controlBtn.clicked.connect(self.startOrStop)  # type: ignore

        self.batteryPlots = BatTimeseriesCanvas()
        self.batteryPlots.draw()
        self.batmap.render()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.turnLabel, 0, 0)
        layout.addWidget(self.batmap, 1, 0)
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(self.controlBtn)
        buttonLayout.addWidget(self.resetBtn)
        buttonLayout.addWidget(self.exportBtn)
        buttonLayout.addWidget(usageLabel)
        buttonLayout.addWidget(self.statsLabel)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout, 1, 1)
        graphLayout = QtWidgets.QHBoxLayout()
        graphLayout.addWidget(self.batteryPlots)
        layout.addLayout(graphLayout, 2, 0, 1, 2)
        self.setLayout(layout)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W:
            self.close()
        if event.key() == Qt.Key.Key_S:
            self.startOrStop()
        elif event.key() in NUMERICAL_KEYS:
            self.userSelectedTurnIndex = NUMERICAL_KEYS.index(event.key())
            connections = self.getOnwardDestinations()
            self.turnLabel.setText(
                f"Selected destination {connections[self.userSelectedTurnIndex]}! "
                "Click 'Start' or press 'S' to resume."
            )
        return super().keyPressEvent(event)

    def chooseTurnIndex(self):
        index = self.userSelectedTurnIndex
        self.userSelectedTurnIndex = None
        return index
