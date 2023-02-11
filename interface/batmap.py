import pathlib
from typing import Optional

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform
from PySide6.QtWidgets import QLabel, QWidget

from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile

SIMULATOR_DIRECTORY = pathlib.Path(__file__).parent


class BatMap(QLabel):
    def __init__(self, batgraph: BatGraph, batmobile: BatMobile, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.graph = batgraph
        self.batmobile = batmobile

        self.canvas = QPixmap(960, 640)
        self.canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(self.canvas)
        self.batmobilePix = QPixmap(SIMULATOR_DIRECTORY / "assets" / "batmobile.png")
        self.controlsEnabled = True
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def render(self):
        self.canvas.fill(Qt.GlobalColor.white)
        painter = QPainter(self.canvas)
        self.paintBatMobile(painter)
        painter.end()
        self.setPixmap(self.canvas)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.controlsEnabled:
            if event.key() == Qt.Key.Key_Up:
                self.batmobile.accelerate(0.1)
            elif event.key() == Qt.Key.Key_Down:
                self.batmobile.accelerate(-0.1)
            elif event.key() == Qt.Key.Key_H:
                self.batmobile.halt()
            event.accept()
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if self.controlsEnabled:
            if event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
                self.batmobile.acceleration = 0
            event.accept()
        return super().keyPressEvent(event)

    def paintBatMobile(self, painter):
        transform = QTransform()
        transform.translate(100 + self.batmobile.position, 100 + self.batmobile.position)
        transform.rotate(-45)
        transform.scale(0.8, 0.8)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.batmobilePix)
