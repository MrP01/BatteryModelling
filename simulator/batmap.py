from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget, QLabel


class BatMap(QLabel):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.canvas = QPixmap(640, 480)
        self.canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(self.canvas)

    def render(self):
        self.canvas = self.pixmap()
        painter = QPainter(self.canvas)
        painter.drawLine(0, 0, 50, 50)
        painter.end()
        self.setPixmap(self.canvas)
