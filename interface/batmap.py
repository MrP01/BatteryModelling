import math
import pathlib
from typing import Optional

import matplotlib.pyplot as plt
from PySide6 import QtCore, QtGui, QtMultimedia
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform
from PySide6.QtWidgets import QLabel, QWidget

from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile

INTERFACE_DIRECTORY = pathlib.Path(__file__).parent


class BatMap(QLabel):
    PLAY_SOUND = False

    def __init__(self, batgraph: BatGraph, batmobile: BatMobile, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.graph = batgraph
        self.batmobile = batmobile

        self.canvas = QPixmap(960, 520)
        self.setPixmap(self.canvas)
        self.batmobilePix = QPixmap(INTERFACE_DIRECTORY / "assets" / "batmobile-outlined.png")
        self.controlsEnabled = True
        self.backgroundColor = self.palette().color(self.backgroundRole())
        self.themeColors = [c["color"] for c in plt.rcParams["axes.prop_cycle"]]
        plt.rcParams["figure.facecolor"] = self.backgroundColor.name()
        plt.rcParams["axes.facecolor"] = self.backgroundColor.name()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.nodeSize = 12 if len(self.graph.nodes) > 30 else 30

        if self.PLAY_SOUND:
            self.effect = QtMultimedia.QSoundEffect()
            self.effect.setSource(QtCore.QUrl.fromLocalFile(INTERFACE_DIRECTORY / "assets" / "vroom-vroom.wav"))

    def render(self) -> None:
        self.canvas.fill(self.backgroundColor)
        painter = QPainter(self.canvas)
        self.paintBatGraph(painter)
        self.paintBatMobile(painter)
        painter.end()
        self.setPixmap(self.canvas)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.controlsEnabled:
            if event.key() == Qt.Key.Key_Up:
                if self.PLAY_SOUND and self.batmobile.velocity == 0:
                    self.effect.play()
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

    def paintBatMobile(self, painter: QPainter) -> None:
        src = self.graph.nodes[self.batmobile.sourceNode]
        dest = self.graph.nodes[self.batmobile.destinationNode]
        edge = self.graph.edges[self.batmobile.sourceNode, self.batmobile.destinationNode]
        x = self.X(src["x"] + self.batmobile.position / edge["length"] * (dest["x"] - src["x"]))
        y = self.Y(src["y"] + self.batmobile.position / edge["length"] * (dest["y"] - src["y"]))
        dy, dx = self.Y(dest["y"]) - self.Y(src["y"]), self.X(dest["x"]) - self.X(src["x"])
        transform = QTransform()
        transform.translate(x, y)
        transform.rotate(math.degrees(math.atan2(dy, dx)) - 90)
        transform.translate(-38, -40)
        transform.scale(0.6, 0.6)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.batmobilePix)

    def paintBatGraph(self, painter: QPainter) -> None:
        originalPen = painter.pen()
        linePen = QtGui.QPen()
        linePen.setWidth(8)
        linePen.setColor(Qt.GlobalColor.white)
        painter.setPen(linePen)
        for A, B in self.graph.edges():
            nodeA, nodeB = self.graph.nodes[A], self.graph.nodes[B]
            painter.drawLine(self.X(nodeA["x"]), self.Y(nodeA["y"]), self.X(nodeB["x"]), self.Y(nodeB["y"]))

        pen = QtGui.QPen()
        pen.setWidth(10)
        pen.setColor(QtGui.QColor(self.themeColors[0]))
        brush = QtGui.QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        for node, data in self.graph.nodes(data=True):
            brush.setColor(QtGui.QColor("#e2dd00") if data["charger"] else Qt.GlobalColor.white)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(
                self.X(data["x"]) - self.nodeSize // 2,
                self.Y(data["y"]) - self.nodeSize // 2,
                self.nodeSize,
                self.nodeSize,
            )
            painter.setPen(originalPen)
            painter.drawText(
                self.X(data["x"]) - self.nodeSize / 6,
                self.Y(data["y"]) + self.nodeSize / 6,
                str(node)[:1],
            )

    def X(self, x):
        return (x - self.graph.center[0]) * 0.9 * self.canvas.width() / self.graph.maxDx + 960 // 2

    def Y(self, y):
        return -(y - self.graph.center[1]) * 0.9 * self.canvas.height() / self.graph.maxDy + 520 // 2

    def highlightNode(self, name) -> None:
        data = self.graph.nodes.get(name)
        if data is None:
            data = self.graph.nodes.get(int(name))
        painter = QPainter(self.canvas)
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor(self.themeColors[2]))
        painter.setPen(pen)
        painter.drawEllipse(
            QtCore.QPoint(self.X(data["x"]), self.Y(data["y"])),
            self.nodeSize * 1.2,
            self.nodeSize * 1.2,
        )
        painter.end()
        self.setPixmap(self.canvas)

    def drawRoute(self, route) -> None:
        painter = QPainter(self.canvas)
        pen = QtGui.QPen()
        pen.setWidth(12)
        pen.setColor(Qt.GlobalColor.darkBlue)
        painter.setPen(pen)
        last = QtCore.QPoint(self.X(self.graph.nodes[route[0]]["x"]), self.Y(self.graph.nodes[route[0]]["y"]))
        for node in route[1:]:
            data = self.graph.nodes.get(node)
            painter.drawLine(last, QtCore.QPoint(self.X(data["x"]), self.Y(data["y"])))
            last = QtCore.QPoint(self.X(data["x"]), self.Y(data["y"]))
        painter.end()
        self.setPixmap(self.canvas)
