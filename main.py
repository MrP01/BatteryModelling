#!/usr/bin/env python
import sys

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt

from simulator.batmap import BatMap


class MainWindow(QtWidgets.QWidget):
    """Our Main Window Class that hosts all sub-widgets and has overall control over the GUI.
    All the simulation-related graphical items and code should be located in simulator/ to keep
    this file as short and clean as possible.
    """

    def __init__(self) -> None:
        super().__init__()

    def buildUI(self):
        self.batmap = BatMap()
        self.batmap.render()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.batmap)
        # layout.addWidget(QtWidgets.QPushButton("Hello"))
        self.setLayout(layout)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W:
            self.close()
        return super().keyPressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    mainWindow = MainWindow()
    mainWindow.buildUI()
    mainWindow.resize(800, 600)
    mainWindow.show()
    sys.exit(app.exec())
