from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from interface.batmap import BatMap
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

        self.batmap.render()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.batmap)
        layout.addWidget(self.controlBtn)
        self.setLayout(layout)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W:
            self.close()
        if event.key() == Qt.Key.Key_S:
            self.startOrStop()
        return super().keyPressEvent(event)
