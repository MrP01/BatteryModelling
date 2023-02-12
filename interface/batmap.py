import math
import pathlib
from typing import Optional

import matplotlib.pyplot as plt
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
        self.setPixmap(self.canvas)
        self.batmobilePix = QPixmap(SIMULATOR_DIRECTORY / "assets" / "batmobile-outlined.png")
        self.controlsEnabled = True
        self.backgroundColor = self.palette().color(self.backgroundRole())
        self.themeColors = [c["color"] for c in plt.rcParams["axes.prop_cycle"]]
        plt.rcParams["figure.facecolor"] = self.backgroundColor.name()
        plt.rcParams["axes.facecolor"] = self.backgroundColor.name()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def render(self):
        self.canvas.fill(self.backgroundColor)
        painter = QPainter(self.canvas)
        self.paintBatGraph(painter)
        self.paintBatMobile(painter)
        painter.end()
        self.setPixmap(self.canvas)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.controlsEnabled:
            if event.key() == Qt.Key.Key_Up:
                self.batmobile.accelerate(self.batmobile.currentJump)
            elif event.key() == Qt.Key.Key_Down:
                self.batmobile.accelerate(-self.batmobile.currentJump)
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

    def paintBatMobile(self, painter: QPainter):
        src = self.graph.nodes[self.batmobile.sourceNode]
        dest = self.graph.nodes[self.batmobile.destinationNode]
        edge = self.graph.edges[self.batmobile.sourceNode, self.batmobile.destinationNode]
        x = src["lat"] + self.batmobile.position / edge["distance"] * (dest["lat"] - src["lat"])
        y = src["long"] + self.batmobile.position / edge["distance"] * (dest["long"] - src["long"])
        transform = QTransform()
        transform.translate(x, y)
        transform.rotate(math.degrees(math.atan2(dest["long"] - src["long"], dest["lat"] - src["lat"])) - 90)
        transform.translate(-38, -40)
        transform.scale(0.6, 0.6)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.batmobilePix)

    def paintBatGraph(self, painter: QPainter):
        originalPen = painter.pen()
        linePen = QtGui.QPen()
        linePen.setWidth(2)
        linePen.setColor(Qt.GlobalColor.white)
        painter.setPen(linePen)
        for A, B in self.graph.edges():
            nodeA, nodeB = self.graph.nodes[A], self.graph.nodes[B]
            painter.drawLine(nodeA["lat"], nodeA["long"], nodeB["lat"], nodeB["long"])

        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtGui.QColor(self.themeColors[0]))
        brush = QtGui.QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        for node, data in self.graph.nodes(data=True):
            brush.setColor(QtGui.QColor("#e2dd00") if data["charger"] else Qt.GlobalColor.white)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(data["lat"] - 15, data["long"] - 15, 30, 30)
            painter.setPen(originalPen)
            painter.drawText(data["lat"] - 5, data["long"] + 5, node)
