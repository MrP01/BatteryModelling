import pathlib
from typing import Optional

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform
from PySide6.QtWidgets import QLabel, QWidget

from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile

SIMULATOR_DIRECTORY = pathlib.Path(__file__).parent


class BatMobileDrawable:
    def __init__(self, batmobile: BatMobile) -> None:
        pass


class BatMap(QLabel):
    def __init__(self, batgraph: BatGraph, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.graph = batgraph
        self.canvas = QPixmap(960, 640)
        self.canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(self.canvas)
        self.batmobilePix = QPixmap(SIMULATOR_DIRECTORY / "assets" / "batmobile.png")

    def render(self):
        # self.canvas = self.pixmap()
        painter = QPainter(self.canvas)
        # painter.drawLine(0, 0, 50, 50)

        transform = QTransform()
        transform.translate(100, 100)
        transform.rotate(-45)
        transform.scale(0.8, 0.8)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.batmobilePix)
        painter.end()

        self.setPixmap(self.canvas)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        # if event.key() == Qt.Key.Key_Up:
        #     self.batmobile.drive()
        return super().keyPressEvent(event)
