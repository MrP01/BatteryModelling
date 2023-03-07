"""The graphical interface / visualisation layer of our simulation!"""
import random

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThreadPool

from interface.batmap import BatMap
from interface.graphs import BatTimeseriesCanvas
from simulator.batgraph import BatGraph
from simulator.optimiser import Optimiser
from simulator.simulation import Simulation

NUMERICAL_KEYS = (Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4, Qt.Key.Key_5)


class MainWindow(Simulation, QtWidgets.QWidget):
    """Our Main Window Class that hosts all sub-widgets and has overall control over the GUI.
    All the simulation-related graphical items and code should be located in simulator/ to keep
    this file as short and clean as possible.
    I am a subclass of the Simulation class.
    """

    STEPS_PER_FRAME = 25

    def __init__(self, locality="Jericho, Oxfordshire, England, United Kingdom"):
        super().__init__(graph=BatGraph.fromName(locality))
        self.batmap = BatMap(self.batgraph, self.batmobile, self)
        self.setWindowTitle("Battery Modelling in the BatMobile")
        self.threadPool = QThreadPool()
        self.userSelectedTurnIndex = None
        self.optimiser = None

    def iterate(self):
        """The iteration method of the simulation, representing a single numerical integration step in time by dt.
        We slightly modify it here on the visualisation layer, but our superclass's iterate() method is still called by
        super().iterate().
        """
        if (
            self.userSelectedTurnIndex is None
            and self.batmobile.position >= self.batgraph.edges[self.currentEdge()]["length"]
        ):
            print("Turning time")
            self.turnLabel.setText("Where would you like to turn? Press 1, 2, 3, etc.")
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

    def iterateOptimiser(self):
        if self.optimiser is None:
            self.optimiser = Optimiser(self.batgraph)
            self.optimiser.initialise(self.sourceDrowdown.currentText(), self.destinationDropdown.currentText())
        else:
            self.optimiser.mcmcStep()
        self.batmap.render()
        self.batmap.drawRoute(self.optimiser.route)
        if self.optimiseBtn.text() != "Monte-Carlo away":
            QtCore.QTimer.singleShot(0, self.iterateOptimiser)

    def updatePlots(self):
        """Updates the plots and redraws them. This is an expensive operation, so we run it outside the main thread."""
        measurement = self.batmobile.battery.measurement()
        measurement.time = self.totalTimeElapsed
        # self.batteryPlots.addMeasurement(measurement)
        # TODO: could add finely-grained data here in batch (instead of just one measurement!)
        self.threadPool.start(lambda: self.batteryPlots.addMeasurement(measurement))

    def startOrStop(self):
        if self.controlBtn.text() == "Start":
            self.iterationTimerId = self.startTimer(20)
            self.controlBtn.setText("Stop")
            self.batmap.setFocus()
        else:
            self.killTimer(self.iterationTimerId)
            self.controlBtn.setText("Start")

    def startOptimiser(self):
        if self.optimiseBtn.text() == "Monte-Carlo away":
            # self.optimisingTimerId = self.startTimer(250)
            self.optimiseBtn.setText("Stop it!")
            QtCore.QTimer.singleShot(0, self.iterateOptimiser)
        else:
            # self.killTimer(self.optimisingTimerId)
            self.optimiseBtn.setText("Monte-Carlo away")

    def timerEvent(self, event: QtCore.QTimerEvent):
        self.iterate()
        # if self.controlBtn.text() == "Stop":
        #     self.iterate()
        # else:
        #     self.iterateOptimiser()
        #     # self.threadPool.start(self.iterateOptimiser)
        return super().timerEvent(event)

    def buildUI(self):
        self.controlBtn = QtWidgets.QPushButton("Start", self)
        self.resetBtn = QtWidgets.QPushButton("Reset", self)
        self.exportBtn = QtWidgets.QPushButton("Export", self)
        self.optimiseBtn = QtWidgets.QPushButton("Monte-Carlo away", self)
        self.singleOptimiseBtn = QtWidgets.QPushButton("Single MCMC-step", self)
        usageLabel = QtWidgets.QLabel(
            "Controls:\n"
            "Click 'Start' to begin the simulation.\n"
            "Use Up/Down arrow keys to drive.\n"
            "Press 'H' to halt the car.\n"
            "Press 'S' as a shortcut to start/stop."
        )
        self.statsLabel = QtWidgets.QLabel()
        self.turnLabel = QtWidgets.QLabel("Welcome to the Electric Vehicle Simulator.")
        self.turnLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sourceDrowdown = QtWidgets.QComboBox(self)
        self.destinationDropdown = QtWidgets.QComboBox(self)
        self.sourceDrowdown.addItems(list(map(str, self.batgraph.nodes)))
        self.destinationDropdown.addItems(list(map(str, self.batgraph.nodes)))
        self.sourceDrowdown.setCurrentText(str(self.batmobile.sourceNode))
        self.destinationDropdown.setCurrentText(str(1273290289))
        self.controlBtn.clicked.connect(self.startOrStop)  # type: ignore
        self.optimiseBtn.clicked.connect(self.startOptimiser)  # type: ignore
        self.singleOptimiseBtn.clicked.connect(self.iterateOptimiser)  # type: ignore
        self.sourceDrowdown.currentTextChanged.connect(self.handleSourceDestinationChange)  # type: ignore
        self.destinationDropdown.currentTextChanged.connect(self.handleSourceDestinationChange)  # type: ignore

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
        buttonLayout.addWidget(QtWidgets.QLabel("Source:"))
        buttonLayout.addWidget(self.sourceDrowdown)
        buttonLayout.addWidget(QtWidgets.QLabel("Destination:"))
        buttonLayout.addWidget(self.destinationDropdown)
        buttonLayout.addWidget(self.optimiseBtn)
        buttonLayout.addWidget(self.singleOptimiseBtn)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout, 1, 1)
        # graphLayout = QtWidgets.QHBoxLayout()
        # graphLayout.addWidget(self.batteryPlots)
        # layout.addLayout(graphLayout, 2, 0, 1, 2)
        self.setLayout(layout)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W:
            self.close()
        if event.key() == Qt.Key.Key_S:
            self.startOrStop()
        elif event.key() == Qt.Key.Key_R:
            nodes = list(self.batgraph.nodes)
            self.batmobile.sourceNode = random.choice(nodes)
            self.batmobile.destinationNode = next(self.batgraph.neighbors(self.batmobile.sourceNode))
            self.batmobile.position = 0
            self.batmap.render()
            self.optimiser = None
            self.sourceDrowdown.setCurrentText(str(self.batmobile.sourceNode))
            self.iterateOptimiser()
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
        self.turnLabel.setText("Continue driving")
        return index

    def handleSourceDestinationChange(self, name):
        self.optimiser = None
        self.batmap.highlightNode(name)
